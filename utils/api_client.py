import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

JSEARCH_HOST = "jsearch.p.rapidapi.com"
JSEARCH_BASE = "https://jsearch.p.rapidapi.com"

def get_api_key():
    key = os.getenv("JSEARCH_API_KEY", "")
    if not key:
        try:
            key = st.secrets["JSEARCH_API_KEY"]
        except Exception:
            pass
    return key

def search_jobs_for_company(company, job_title="cybersecurity", location="USA", num_pages=1):
    api_key = get_api_key()
    if not api_key or api_key == "your_jsearch_api_key_here":
        return _demo_jobs(company, job_title)

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": JSEARCH_HOST,
    }

    query = f"{job_title} jobs in USA"
    params = {
        "query": query,
        "num_pages": "1",
        "country": "us",
        "date_posted": "month",
    }

    try:
        response = requests.get(
            f"{JSEARCH_BASE}/search-v2",
            headers=headers,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        raw = data.get("data", {})
        if isinstance(raw, dict):
            raw_jobs = raw.get("jobs", [])
        elif isinstance(raw, list):
            raw_jobs = raw
        else:
            raw_jobs = []

        if not raw_jobs:
            return _demo_jobs(company, job_title)

        return [_normalize_job(job, company) for job in raw_jobs[:3]]

    except Exception:
        return _demo_jobs(company, job_title)

def _normalize_job(raw, company):
    return {
        "company": raw.get("employer_name", company),
        "title": raw.get("job_title", ""),
        "location": _format_location(raw),
        "salary": _format_salary(raw),
        "education_required": raw.get("job_required_education", {}).get("required_credential", "Not specified") if isinstance(raw.get("job_required_education"), dict) else "Not specified",
        "certifications_required": _extract_certs(raw),
        "skills_required": _extract_skills(raw),
        "link": raw.get("job_apply_link", ""),
        "date_posted": str(raw.get("job_posted_at_datetime_utc", ""))[:10],
        "description": raw.get("job_description", "")[:1000],
        "employment_type": raw.get("job_employment_type", ""),
        "is_remote": raw.get("job_is_remote", False),
    }

def _format_location(raw):
    if raw.get("job_is_remote"):
        return "Remote"
    parts = [p for p in [raw.get("job_city",""), raw.get("job_state",""), raw.get("job_country","")] if p]
    return ", ".join(parts) if parts else "Not specified"

def _format_salary(raw):
    min_s = raw.get("job_min_salary")
    max_s = raw.get("job_max_salary")
    salary_str = raw.get("job_salary_string", "")
    period = raw.get("job_salary_period", "YEAR")
    if min_s and max_s:
        return f"${int(min_s):,} - ${int(max_s):,} / {period.lower()}"
    elif salary_str:
        return salary_str
    return "Not listed"

def _extract_certs(raw):
    desc = raw.get("job_description", "").lower()
    cert_keywords = ["Security+","CISSP","CEH","CISM","CISA","CCNA","Network+",
                     "AWS Certified","CompTIA","Linux+","CySA+","OSCP","GIAC"]
    found = [c for c in cert_keywords if c.lower() in desc]
    return ", ".join(found) if found else "None specified"

def _extract_skills(raw):
    skills_list = raw.get("job_required_skills") or []
    if skills_list:
        return ", ".join(skills_list[:10])
    desc = raw.get("job_description", "").lower()
    common = ["Python","Linux","Wireshark","Nmap","SIEM","Splunk","Networking",
              "Firewall","Cloud","AWS","Azure","Docker","Bash","PowerShell","SQL"]
    found = [s for s in common if s.lower() in desc]
    return ", ".join(found[:10]) if found else "See description"

def _demo_jobs(company, job_title):
    return [
        {
            "company": company,
            "title": "Cybersecurity Analyst",
            "location": "New York, NY",
            "salary": "$65,000 - $85,000 / year",
            "education_required": "Bachelor's Degree",
            "certifications_required": "Security+, CompTIA A+",
            "skills_required": "Python, Networking, Wireshark, SIEM",
            "link": "",
            "date_posted": "2026-06-24",
            "description": "Demo job - API key not loaded.",
            "employment_type": "FULLTIME",
            "is_remote": False,
        },
    ]
