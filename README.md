# Job Matcher

## Overview

Job Matcher is a web application that helps users find jobs that match their skills and experiences. It integrates with the Adzuna API to fetch job listings, web scrapes job descriptions, and uses the Gemini API to refine and extract relevant job requirements. The application then calculates a matching score using cosine similarity between user skills/experiences and job requirements, providing users with a ranked list of job opportunities.

## Features

- **Job Search:** Fetch job listings from Adzuna based on the user's location.
- **Job Description Extraction:** Scrape and extract job descriptions from job listing URLs.
- **Job Requirement Refinement:** Use Gemini API to refine and extract specific job requirements.
- **Skill Matching:** Calculate matching scores between user skills/experiences and job requirements using cosine similarity.
- **Job Ranking:** Provide a ranked list of job opportunities based on the matching score.

## Prerequisites

- Python 3.x
- Flask
- Requests
- Scikit-learn
- BeautifulSoup
- Google Generative AI API
- A valid Adzuna API key
- A valid Google API key

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SharanyaBasu/SkillSync.git
   cd SkillSync
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File:**

   Create a `.env` file in the root directory of the project and add the following environment variables:
   ```
   ADZUNA_APP_ID=your_adzuna_app_id
   ADZUNA_API_KEY=your_adzuna_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. **Run the Flask Application:**
   ```bash
   python app.py
   ```

2. **Access the API:**

   You can interact with the API endpoint to match jobs using a POST request:
   ```bash
   curl -X POST http://localhost:8000/api/match_jobs -H "Content-Type: application/json" -d '{
     "location": "toronto",
     "user_skills": "Python, Flask, Web Scraping",
     "user_experiences": "Developed web applications using Flask, Experienced in web scraping with BeautifulSoup"
   }'
   ```

## API Endpoints

- **`/api/match_jobs`**

  **Method:** POST
  
  **Description:** Accepts user skills and experiences, and location. Returns a list of job opportunities with matching scores.

  **Request Body:**
  ```json
  {
    "location": "string",
    "user_skills": "string",
    "user_experiences": "string"
  }
  ```

  **Response:**
  ```json
  {
    "jobs": [
      {
        "title": "string",
        "company": "string",
        "location": "string",
        "description": "string",
        "matching_score": "number",
        "url": "string"
      }
    ]
  }
  ```

## Project Structure

- **`app.py`**: Main Flask application file that handles API requests and integrates with Adzuna and the Gemini API.
- **`extractor.py`**: Contains functions to fetch job details, extract and refine job descriptions using web scraping and the Gemini API.
- **`.env`**: Stores sensitive environment variables like API keys.
