# 2026 FEC Congressional Candidate Data Collection

A Python project that retrieves 2026 U.S. Senate and House of Representatives candidate information from the [Federal Election Commission (FEC) OpenFEC API](https://api.open.fec.gov/developers/), converts the JSON response into pandas DataFrames, and exports the results to CSV files.

## Project objectives

- Phase A: Campaign finance tracker (in progress)
- Phase B: Polls vs. election results
- Phase C: Geospatial and demographic analysis (county level)
- Phase D: Predictive modeling (baseline + gradient boosting, spatial cross-validation)

## Technologies

- Python 3
- `requests` — HTTP requests and API responses
- `pandas` — DataFrames and CSV exports
- `python-dotenv` — environment variable loading

## Setup

1. Clone or download the project and open its directory in a terminal.
2. Install the dependencies:

   ```bash
   pip install requests pandas python-dotenv
   ```

3. Obtain an API key from the [OpenFEC API documentation](https://api.open.fec.gov/developers/).
4. Create a file named `fec.env` in the project directory:

   ```dotenv
   FEC_API_KEY=your_actual_api_key_here
   ```

5. Run the Python script (replace `main.py` with your actual filename):

   ```bash
   python main.py
   ```

**Security:** Do not commit `fec.env` or your API key to GitHub. Add this to `.gitignore`:

```gitignore
fec.env
.env
__pycache__/
```

## API endpoint and parameters

**Endpoint:** `https://api.open.fec.gov/v1/candidates/`

| Parameter | Value | Purpose |
| --- | --- | --- |
| `api_key` | Loaded from `FEC_API_KEY` | Authenticates the request |
| `election_year` | `2026` | Selects the election cycle |
| `office` | `S` or `H` | Senate or House candidates |
| `has_raised_funds` | `True` | Filters for candidates who have raised funds |
| `per_page` | `100` | Requests up to 100 records per page |

The script loops over `S` and `H`, sending a separate API request for each office.

## Processing workflow

1. Load the API key using `load_dotenv("fec.env")` and `os.getenv("FEC_API_KEY")`.
2. Create a dictionary of API query parameters.
3. Send the request with `requests.get(URL, params=query_settings, timeout=30)`.
4. Check the response with `response.raise_for_status()`.
5. Convert the response to Python data with `response.json()`.
6. Read `election_data["pagination"]["count"]` for the total number of matching candidates and `len(election_data["results"])` for the current page's records.
7. Convert `election_data["results"]` to a pandas DataFrame.
8. Export the DataFrame to CSV with `index=False`.

## Output files

| File | Contents |
| --- | --- |
| `senate_candidates.csv` | Senate candidate records returned by the API |
| `house_candidates.csv` | House candidate records returned by the API |

The exact columns depend on the fields returned by the OpenFEC API.

## Error handling

The script checks for a missing API key and raises a `ValueError` when it is unavailable. It also uses `raise_for_status()` to identify unsuccessful HTTP responses, catches request-related exceptions (including network failures and timeouts), and handles file-writing errors when exporting CSV files.

## Current limitations

- The FEC tracks money, not votes. It doesn't record who won a primary, so
  candidate lists include primary losers.
- Fundraising data lags: some late donations aren't reported until after the election.

## Possible future improvements

- Implement pagination to collect all matching candidate records.
- Add data cleaning, validation, and duplicate checks.
- Analyze candidates by state, party, and office.
- Create visualizations or an interactive dashboard.
- Add automated tests and reproducible dependency management.

## Data source

Federal Election Commission, [OpenFEC API](https://api.open.fec.gov/developers/).

This project is for educational and data-analysis purposes and is not affiliated with the FEC.
