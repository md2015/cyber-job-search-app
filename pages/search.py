import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.companies import COMPANIES, CYBER_JOB_TITLES
from utils.api_client import search_jobs_for_company
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
        selected_companies = st.multiselect("Select Companies", options=COMPANIES, default=COMPANIES[:5])
        job_keyword = st.selectbox("Job Category", options=CYBER_JOB_TITLES, index=0)
        location_filter = st.text_input("Location Filter", value="USA")

    profile = st.session_state.get("user_profile", DEFAULT_PROFILE)

    if not selected_companies:
        st.info("Select at least one company in the sidebar.")
        return

    if st.button(f"🚀 Search {len(selected_companies)} Companies", type="primary"):
        all_jobs = []
        progress = st.progress(0, text="Starting...")
        for i, company in enumerate(selected_companies):
            progress.progress((i+1)/len(selected_companies), text=f"Searching {company}...")
            jobs = search_jobs_for_company(company=company, job_title=job_keyword, location=location_filter)
            all_jobs.extend(jobs)
        progress.empty()
        if all_jobs:
            st.session_state["search_results"] = batch_match(all_jobs, profile)
            st.success(f"Found {len(all_jobs)} jobs.")
        else:
            st.warning("No results found.")

    results = st.session_state.get("search_results", [])
    if not results:
        st.info("Run a search to see results.")
        return

    st.markdown("### Results")
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
