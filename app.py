import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Career Enhancement Job Search", page_icon="🎓", layout="wide")

from app_pages import search, dashboard, export_page

st.sidebar.title("🎓 Career Enhancement Job Search")
st.sidebar.markdown("Bronx Community College")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", ["🔍 Job Search", "📊 Dashboard", "📤 Export Results"])

if page == "🔍 Job Search":
    search.render()
elif page == "📊 Dashboard":
    dashboard.render()
elif page == "📤 Export Results":
    export_page.render()
