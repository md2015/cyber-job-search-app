import re
import streamlit as st
from data.departments import DEPARTMENTS, ALL_DEPARTMENTS_LABEL, ALL_MAJORS_LABEL
from utils.api_client import search_jobs_bulk

US_STATES = [
    "Remote", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii",
    "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
    "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming"
]

COUNTRIES = {
    "United States": "us",
    "Canada": "ca",
    "United Kingdom": "gb",
    "India": "in",
    "Australia": "au",
    "Germany": "de",
    "Bangladesh": "bd",
}


def clean_description(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def inject_css():
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
        }
        html, body, [class*="css"] {
            font-size: 17px;
        }
        .bcc-header {
            padding: 1.5rem 0 1rem 0;
            border-bottom: 4px solid #1a4d8f;
            margin-bottom: 1.5rem;
        }
        .bcc-header h1 {
            color: #0d2b54;
            font-weight: 800;
            font-size: 2.1rem;
            margin-bottom: 0.3rem;
        }
        .bcc-header p {
            color: #2c2c2c;
            font-size: 1.1rem;
            margin-top: 0;
        }
        .job-title {
            font-size: 1.3rem;
            font-weight: 800;
            color: #000000;
        }
        .job-meta {
            color: #1a1a1a;
            font-size: 1rem;
            line-height: 1.6;
        }
        .job-meta b {
            color: #000000;
        }
        .job-salary {
            display: inline-block;
            background-color: #d9ead3;
            color: #0f4d1a;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 0.25rem 0.8rem;
            border: 1px solid #2e7d32;
            border-radius: 12px;
            margin: 0.5rem 0;
        }
        .results-banner {
            background-color: #0d2b54;
            color: #ffffff;
            padding: 0.8rem 1.2rem;
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 1.2rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid #b0b8c1 !important;
            border-radius: 8px !important;
        }
        div.stButton > button, .stLinkButton > a {
            background-color: #0d2b54 !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            border: none !important;
            padding: 0.5rem 1.2rem !important;
        }
        div.stButton > button:hover, .stLinkButton > a:hover {
            background-color: #15396f !important;
        }
        label, .stSelectbox label, .stTextInput label {
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 1.02rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def format_location(job):
    city = job.get("job_city")
    state = job.get("job_state")
    if job.get("job_is_remote"):
        return "Remote"
    if city and state:
        return f"{city}, {state}"
    if state:
        return state
    if city:
        return city
    return "Location not specified"


def format_salary(job):
    salary_string = job.get("job_salary_string")
    min_sal = job.get("job_min_salary")
    max_sal = job.get("job_max_salary")
    if salary_string:
        return salary_string
    if min_sal and max_sal:
        return f"${min_sal:,.0f} - ${max_sal:,.0f}"
    return None


def render():
    inject_css()

    st.markdown("""
        <div class="bcc-header">
            <h1>Career Enhancement Job Search</h1>
            <p>Live job openings for every major and department at Bronx Community College.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox("Department", list(DEPARTMENTS.keys()))
    with col2:
        major = st.selectbox("Major / Program", DEPARTMENTS[department])

    job_title = st.text_input(
        "Job Title (optional)",
        placeholder="e.g. Registered Nurse, Accountant, Network Technician, Paralegal..."
    )

    col3, col4 = st.columns(2)
    with col3:
        country = st.selectbox("Country", list(COUNTRIES.keys()))
    with col4:
        state = st.selectbox("State", US_STATES) if country == "United States" else st.text_input("Region / City (optional)")

    if st.button("Search Jobs Now", type="primary"):
        if job_title.strip():
            query_term = job_title.strip()
        elif major != ALL_MAJORS_LABEL:
            query_term = major
        elif department != ALL_DEPARTMENTS_LABEL:
            query_term = department
        else:
            query_term = "entry level"

        if country == "United States":
            location_term = "United States" if state == "Remote" else state
            is_remote = (state == "Remote")
        else:
            location_term = state.strip() if state else country
            is_remote = False

        with st.spinner("Searching live job listings..."):
            jobs = search_jobs_bulk(
                query=query_term,
                location=location_term,
                remote=is_remote,
                country_code=COUNTRIES[country],
            )

        if not jobs:
            st.warning("No jobs found. Try a broader job title or a different location.")
        else:
            st.markdown(f'<div class="results-banner">Found {len(jobs)} job listing(s)</div>', unsafe_allow_html=True)

            for job in jobs:
                title = clean_description(job.get("job_title", "Untitled Position"))
                company = clean_description(job.get("employer_name", "Not specified"))
                location = format_location(job)
                salary = format_salary(job)
                description = clean_description(job.get("job_description", ""))
                apply_link = job.get("job_apply_link")

                with st.container(border=True):
                    st.markdown(f'<div class="job-title">{title}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="job-meta"><b>Company:</b> {company}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="job-meta"><b>Location:</b> {location}</div>', unsafe_allow_html=True)
                    if salary:
                        st.markdown(f'<div class="job-salary">{salary}</div>', unsafe_allow_html=True)
                    if description:
                        trimmed = description[:400] + ("..." if len(description) > 400 else "")
                        st.write(trimmed)
                    if apply_link:
                        st.link_button("Apply Now", apply_link)
