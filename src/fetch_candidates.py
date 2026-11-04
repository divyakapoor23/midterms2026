import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Constants: fixed values, safe at the top of the file
PROJECT_ROOT = Path(__file__).resolve().parents[1]
URL = "https://api.open.fec.gov/v1/candidates/"
ELECTION_YEAR = 2026
PER_PAGE = 100
TIMEOUT_SECONDS = 30
PAUSE_SECONDS = 0.5  # short pause between requests, to be polite to the API

OFFICES = {
    "S": PROJECT_ROOT / "data/raw/senate_candidates.csv",
    "H": PROJECT_ROOT / "data/raw/house_candidates.csv",
}


def load_api_key():
    """Load the FEC API key from the env file. Stop with a clear error if it's missing."""
    env_path = PROJECT_ROOT / "fec.env"
    load_dotenv(env_path)
    api_key = os.getenv("FEC_API_KEY")
    if not api_key:
        raise RuntimeError(f"FEC_API_KEY not found. Set it in {env_path} or your environment.")
    return api_key


def fetch_page(office, page, api_key):
    """Request one page of candidates for one office. Returns the JSON as a dict."""
    query_settings = {
        "api_key": api_key,
        "election_year": ELECTION_YEAR,
        "office": office,
        "has_raised_funds": True,
        "per_page": PER_PAGE,
        "page": page,
    }
    response = requests.get(URL, params=query_settings, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()  # error for 4xx/5xx responses
    return response.json()


def fetch_all_candidates(office, api_key):
    """Fetch every page for one office. Returns a list of all candidates."""
    first_page = fetch_page(office, 1, api_key)
    total_pages = first_page["pagination"]["pages"]
    expected_count = first_page["pagination"]["count"]

    all_candidates = list(first_page["results"])
    print(f"[{office}] page 1/{total_pages}")

    for page in range(2, total_pages + 1):
        time.sleep(PAUSE_SECONDS)
        data = fetch_page(office, page, api_key)
        all_candidates.extend(data["results"])
        print(f"[{office}] page {page}/{total_pages}")

    # Sanity check: did we get everything the API said exists?
    if len(all_candidates) != expected_count:
        print(f"WARNING [{office}]: expected {expected_count}, got {len(all_candidates)}")

    return all_candidates


def save_csv(candidates, filename):
    """Save a list of candidate dicts to a CSV file."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(candidates)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} rows to {filename}")


def main():
    api_key = load_api_key()
    for office, filename in OFFICES.items():
        candidates = fetch_all_candidates(office, api_key)
        save_csv(candidates, filename)


if __name__ == "__main__":
    main()
