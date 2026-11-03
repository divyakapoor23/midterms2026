import os
import requests
from dotenv import load_dotenv
import pandas as pd



load_dotenv("fec.env")
api_key = os.getenv("FEC_API_KEY")
print("FEC_API_KEY loaded:", bool(api_key))

URL = "https://api.open.fec.gov/v1/candidates/"

"""
Make a dictionary of the query settings
Call requests.get(), giving it the URL and passing the dictionary as params=.
Print the response’s status_code.
"""
offices = {
    "S": "senate_candidates.csv",
    "H": "house_candidates.csv"
}

for office, filename in offices.items():
    
    query_settings = {
        "api_key": api_key,
        "election_year": 2026,
        "office": office,
        "has_raised_funds": True,
        "per_page": 100
    }

try:
    response = requests.get(
        URL,
        params = query_settings,
        timeout = 30
    )

    print(f"\nStatus code for {office}:",
          response.status_code)
# Throw an error for unsuccessful HTTP responses
    response.raise_for_status()
    election_data = response.json()
    # Display candidate counts
    print("Total candidates:",
            election_data["pagination"]["count"])

    print("Candidates on this page:",
            len(election_data["results"]))
    df = pd.DataFrame(election_data["results"])

    # Save CSV with error handling
    try:
        df.to_csv(filename, index=False)
        print(f"Successfully saved {filename}")

    except OSError as e:
        print(f"Error creating CSV: {e}")
        raise   

except requests.exceptions.RequestException as e:
        print(f"API request failed for {office}: {e}")
        raise

    