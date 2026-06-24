import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="CyberJobs Intelligence", page_icon="🔐", layout="wide")

from pages import search, dashboard, export_page
from pages import user_profile

st.sidebar.title("🔐 CyberJobs Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", ["🔍 Job Search", "📊 Dashboard", "👤 My Profile", "📥 Export Results"])

if page == "🔍 Job Search":
    search.render()
elif page == "📊 Dashboard":
    dashboard.render()
elif page == "👤 My Profile":
    user_profile.render()
elif page == "📥 Export Results":
    export_page.render()
