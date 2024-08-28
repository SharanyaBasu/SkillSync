from extractor import extract_descriptions_and_details_from_urls

# Define some test URLs
test_urls = [
    'https://www.adzuna.ca/details/4754023532?utm_medium=api&utm_source=379fa6a6',
    'https://www.adzuna.ca/details/4801647400?utm_medium=api&utm_source=379fa6a6'
]

def main():
    # Extract descriptions and details using the updated function
    refined_descriptions, details = extract_descriptions_and_details_from_urls(test_urls)

    for i, url in enumerate(test_urls):
        print(f"URL: {url}")
        print(f"Title: {details[i].get('title', 'N/A')}")
        print(f"Location: {details[i].get('location', 'N/A')}")
        print(f"Company: {details[i].get('company', 'N/A')}")
        print(f"Description: {refined_descriptions[i]}")
        print("\n" + "-"*40 + "\n")  # Print a separator for better readability

# Run the test
if __name__ == "__main__":
    main()
