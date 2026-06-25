import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.companies import COMPANIES, CYBER_JOB_TITLES
from utils.api_client import search_jobs_bulk

def render():
    st.title("🔍 Cybersecurity Job Search")
    st.markdown("Find real cybersecurity job openings in the USA.")

    with st.sidebar:
        st.header("Search Settings")
        job_keyword = st.selectbox("Job Category", options=CYBER_JOB_TITLES, index=0)
        location = st.text_input("Location", value="USA")
        st.markdown("---")
        st.caption("Each search returns up to 10 real live jobs.")

    if st.button("🚀 Search Jobs Now", type="primary"):
        with st.spinner(f"Searching for {job_keyword} jobs..."):
            jobs = search_jobs_bulk(job_keyword, location)
        if jobs:
            st.session_state["search_results"] = jobs
            st.success(f"Found {len(jobs)} real jobs for **{job_keyword}**.")
        else:
            st.warning("No results found. Try a different category.")

    results = st.session_state.get("search_results", [])

    if not results:
        st.info("Select a job category and click Search.")
        return

    st.markdown("---")
    st.markdown(f"### Results")

    for job in results:
        with st.container():
            st.markdown(f"""
            <div style="border-left:4px solid #2ecc71;padding:12px 16px;
                        margin-bottom:12px;border-radius:4px;
                        background:rgba(46,204,113,0.05);">
                <h4 style="margin:0">{job.get('title','')}</h4>
                <span style="color:#aaa">
                🏢 {job.get('company','')} &nbsp;|&nbsp;
                📍 {job.get('location','')} &nbsp;|&nbsp;
                💰 {job.get('salary','Not listed')} &nbsp;|&nbsp;
                📅 {job.get('date_posted','')}
                </span>
            </div>""", unsafe_allow_html=True)

            with st.expander("View Job Details"):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Education Required**\n\n{job.get('education_required','Not specified')}")
                col2.markdown(f"**Employment Type**\n\n{job.get('employment_type','Not specified')}")
                st.markdown(f"**Certifications**\n\n{job.get('certifications_required','None listed')}")
                st.markdown(f"**Skills**\n\n{job.get('skills_required','See description')}")
                if job.get("description"):
                    st.markdown(f"**Job Summary**\n\n{job.get('description','')[:300]}...")
                st.markdown("---")
                if job.get("link"):
                    st.markdown(f"### [🔗 Apply Now — Click Here]({job['link']})")
                else:
                    st.caption("No direct apply link available.")
