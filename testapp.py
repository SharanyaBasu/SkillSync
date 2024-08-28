import requests  # For making HTTP requests

# URL of the Flask app
FLASK_API_URL = 'http://127.0.0.1:5000/api/match_jobs'

# Hardcoded sample user profile
sample_profile = {
    'location': 'toronto',  # Example location
    # Example skills
    'user_skills': 'Python, machine learning, data analysis, Flask, web scraping'
}

# Function to test the API


def test_match_jobs(profile):
    params = {
        'location': profile['location'],
        'user_skills': profile['user_skills']
    }

    try:
        response = requests.get(FLASK_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Print the response from the API
        data = response.json()
        if 'jobs' in data:
            for job in data['jobs']:
                print(f"Job Title: {job['title']}")
                print(f"Company: {job['company']}")
                print(f"Location: {job['location']}")
                # Print first 200 chars of description
                print(f"Description: {job['description'][:200]}...")
                print(f"Matching Score: {job['matching_score']}")
                print(f"URL: {job['url']}")
                print('-' * 80)
        else:
            print(f"Error: {data.get('error', 'Unknown error')}")
    except requests.RequestException as e:
        print(f"Error testing API: {e}")


# Run the test
test_match_jobs(sample_profile)
