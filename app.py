from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from extractor import extract_descriptions_and_details_from_urls

load_dotenv()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

APP_ID = os.getenv('ADZUNA_APP_ID')
API_KEY = os.getenv('ADZUNA_API_KEY')


def search_jobs(location, results=10):
    url = 'https://api.adzuna.com/v1/api/jobs/ca/search/1'
    params = {
        'app_id': APP_ID,
        'app_key': API_KEY,
        'where': location,
        'results_per_page': results
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, params=params, headers=headers)
    print(f"Request URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        try:
            data = response.json()
            job_urls = [job['redirect_url'] for job in data.get('results', [])]
            return job_urls
        except ValueError:
            print("Failed to parse JSON")
            return None
    else:
        print(f"Error Response: {response.text}")
        return None


def match_skills(user_skills, user_experiences, job_descriptions):
    user_profile = user_skills + " " + user_experiences

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([user_profile] + job_descriptions)
    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    return similarity[0]


@app.route('/api/match_jobs', methods=['POST'])
def match_jobs():
    # Get location from query parameters
    location = request.args.get('location')

    # Get user skills and experiences from the request body
    data = request.get_json()
    user_skills = data.get('user_skills')
    user_experiences = data.get('user_experiences')

    # Check if location and user_skills are provided
    if not location or not user_skills:
        return jsonify({'error': 'Location or user skills not provided'}), 400

    # Fetch job URLs
    job_urls = search_jobs(location)

    if not job_urls:
        return jsonify({'error': 'No job URLs found'}), 500

    # Extract job details and descriptions
    refined_descriptions, job_details = extract_descriptions_and_details_from_urls(job_urls)

    if job_details and refined_descriptions:
        # Generate similarity scores
        matching_scores = match_skills(user_skills, user_experiences, refined_descriptions)  # Note: removed user_experiences from here

        # Prepare results
        result = []
        for i, job in enumerate(job_details):
            job_info = {
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'description': refined_descriptions[i] if i < len(refined_descriptions) else 'N/A',
                'matching_score': matching_scores[i] if i < len(matching_scores) else 0,
                'url': job_urls[i]  # Include URL if needed
            }
            result.append(job_info)

        # Sort by matching score
        result_sorted = sorted(
            result, key=lambda x: x['matching_score'], reverse=True)

        return jsonify({'jobs': result_sorted})
    else:
        return jsonify({'error': 'No job descriptions or details found or API error'}), 500


@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
