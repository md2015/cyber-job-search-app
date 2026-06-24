import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.companies import COMPANIES, CYBER_JOB_TITLES
from utils.api_client import search_jobs_bulk
from utils.matcher import batch_match

DEFAULT_PROFILE = {
    "degrees": ["AAS Cybersecurity and Networking", "BS Computer Science and Information Security"],
    "certifications": ["CompTIA A+", "CompTIA Linux+", "CEH", "IBM Cybersecurity Analyst"],
    "skills": ["Python", "Kali Linux", "Networking", "Wireshark", "Nmap", "Security Fundamentals"],
    "years_experience": 2,
}

def render():
    st.title("🔍 Cybersecurity Job Search")
    with st.sidebar:
        st.header("Search Settings")
        selected_companies = st.multiselect("Filter by Company", options=COMPANIES, default=COMPANIES[:25])
        job_keyword = st.selectbox("Job Category", options=CYBER_JOB_TITLES, index=0)
        st.markdown("---")
        st.caption("One API call returns up to 10 real jobs instantly.")

    profile = st.session_state.get("user_profile", DEFAULT_PROFILE)

    if st.button(f"🚀 Search Jobs Now", type="primary"):
        with st.spinner("Searching for real cybersecurity jobs..."):
            jobs = search_jobs_bulk(job_keyword)
        if jobs:
            st.session_state["search_results"] = batch_match(jobs, profile)
            st.session_state["selected_companies"] = selected_companies
            st.success(f"Found {len(jobs)} real jobs.")
        else:
            st.warning("No results found.")

    results = st.session_state.get("search_results", [])
    selected = st.session_state.get("selected_companies", selected_companies)

    if not results:
        st.info("Click Search Jobs Now to see results.")
        return

    st.markdown("### Results")
    shown = 0
    for job in results:
        score = job.get("match_score", 0)
        status = job.get("match_status", "")
        color = "#2ecc71" if "Yes" in status else ("#f39c12" if "Partial" in status else "#e74c3c")
        st.markdown(f"""<div style="border-left:4px solid {color};padding:10px 16px;margin-bottom:10px;border-radius:4px;">
            <strong>{job.get('title','')}</strong> &nbsp;
            <span style="color:{color}">{status} — {score}%</span><br/>
            🏢 {job.get('company','')} &nbsp;|&nbsp; 📍 {job.get('location','')} &nbsp;|&nbsp; 💰 {job.get('salary','Not listed')}
        </div>""", unsafe_allow_html=True)
        with st.expander("Details"):
            st.write(f"**Education:** {job.get('education_required','Not specified')}")
            st.write(f"**Certs:** {job.get('certifications_required','None listed')}")
            st.write(f"**Skills:** {job.get('skills_required','See description')}")
            if job.get("link"):
                st.markdown(f"[🔗 Apply Now]({job['link']})")
            else:
                st.caption("No apply link available for this job.")
        shown += 1
