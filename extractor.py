import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline
import torch
import google.generativeai as genai 
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

KEYWORDS = [
    'Responsibilities', 'Accountabilities', 'Requirements', 'What we require', 'Duties', 'Skills',
    'Qualifications', 'Experience', 'What you bring', 'What you will do', 'Good to know'
]


def fetch(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_text_after_keyword(text, keywords):
    # Initialize to the length of the text (i.e., no valid keyword found yet)
    min_index = len(text)
    for keyword in keywords:
        index = text.lower().find(keyword.lower())
        if index != -1 and index < min_index:
            min_index = index

    # If min_index was updated, return the text from that index
    if min_index < len(text):
        return text[min_index:].strip()

    return ''


def extract_job_description(url, seen_descriptions):
    html = fetch(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        section = soup.find(
            'section', class_='adp-body mx-4 mb-4 text-sm md:mx-0 md:text-base md:mb-0')
        if not section:
            print(f"No section found for URL: {url}")
            return None

        text = section.get_text(separator=' ', strip=True)
        description = extract_text_after_keyword(text, KEYWORDS)

        if description and description not in seen_descriptions:
            seen_descriptions.add(description)
            return description
    return None


def extract_job_details(url):
    html = fetch(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('h1', class_='mr-3 text-2xl md:text-3xl')
        title = title_tag.text.strip() if title_tag else 'N/A'

        details_div = soup.find(
            'div', class_='p-4 bg-adzuna-green-100 md:rounded-lg md:flex md:items-center')
        location = 'N/A'
        company = 'N/A'

        if details_div:
            table = details_div.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        key = th.get_text(strip=True)
                        value = td.get_text(strip=True)
                        if key.lower() == 'location:':
                            location = value
                        elif key.lower() == 'company:':
                            company = value

        return {'title': title, 'location': location, 'company': company}
    return {'title': 'N/A', 'location': 'N/A', 'company': 'N/A'}


def fetch_all(urls):
    seen_descriptions = set()
    descriptions = []
    details = []
    for url in urls:
        description = extract_job_description(url, seen_descriptions)
        details.append(extract_job_details(url))
        if description:
            descriptions.append(description)
    return descriptions, details


# def extract_descriptions_and_details_from_urls(urls):
#     return fetch_all(urls)

#New new code: 

def refine_description_with_gemini(description):
    prompt = '''
    Read the job description and provide the specific requirements needed for this job in a concise manner. 
    Extract only the relevant qualifications, skills, and experience required for this job.
    Don't use markdown formatting on the response. Return the response in plain text format. 
    '''
    prompt_with_description = prompt + "\n" + description
    try:
        response = model.generate_content(prompt_with_description)
        text_parts = [part.text for part in response.parts]
        return " ".join(text_parts)
    except ValueError as e:
        print(f"Error generating refined description: {str(e)}")
        return description  # Return original if error occurs

def extract_descriptions_and_details_from_urls(urls):
    descriptions, details = fetch_all(urls)
    refined_descriptions = [refine_description_with_gemini(desc) for desc in descriptions]
    return refined_descriptions, details
