"""
JSearch API client (RapidAPI) — used to fetch real, live job postings.
Free tier: 200 requests/month. Monitor usage at rapidapi.com dashboard.
"""

import os
import requests
import streamlit as st

try:
    JSEARCH_API_KEY = st.secrets["JSEARCH_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")

JSEARCH_HOST = "jsearch.p.rapidapi.com"
JSEARCH_URL = f"https://{JSEARCH_HOST}/search-v2"


def search_jobs_bulk(query: str, location: str = "United States", remote: bool = False, num_pages: int = 4, country_code: str = "us"):
    """
    Search live job postings via the JSearch API (search-v2 endpoint).

    Args:
        query: search term — job title, major, or department
        location: state/region/city name, or "United States" for nationwide search
        remote: if True, biases the search toward remote-friendly listings
        num_pages: number of result pages to fetch from JSearch
        country_code: two-letter country code (e.g. "us", "ca", "gb", "in")

    Returns:
        A list of job dicts.
    """

    if not JSEARCH_API_KEY:
        st.error("JSearch API key not found. Please check your Streamlit Secrets or .env file.")
        return []

    headers = {
        "x-rapidapi-key": JSEARCH_API_KEY,
        "x-rapidapi-host": JSEARCH_HOST,
    }

    full_query = f"{query} in {location}" if location else query

    params = {
        "query": full_query,
        "page": "1",
        "num_pages": str(num_pages),
        "country": country_code,
        "date_posted": "all",
    }

    if remote:
        params["remote_jobs_only"] = "true"

    try:
        response = requests.get(JSEARCH_URL, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        data_section = data.get("data", {})

        if isinstance(data_section, list):
            jobs = data_section
        elif isinstance(data_section, dict):
            jobs = data_section.get("jobs", [])
        else:
            jobs = []

        if jobs and not isinstance(jobs[0], dict):
            st.warning("Unexpected API response format (entries are not job objects).")
            return []

        return jobs

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching jobs from JSearch API: {e}")
        return []
    except ValueError:
        st.error("Received an unexpected response from the JSearch API.")
        return []
