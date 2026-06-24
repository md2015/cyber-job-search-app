import streamlit as st

DEFAULT_PROFILE = {
    "degrees": ["AAS Cybersecurity and Networking", "BS Computer Science and Information Security"],
    "certifications": ["CompTIA A+", "CompTIA Linux+", "CEH", "IBM Cybersecurity Analyst"],
    "skills": ["Python", "Kali Linux", "Networking", "Wireshark", "Nmap", "Security Fundamentals"],
    "years_experience": 2,
}

def render():
    st.title("👤 My Profile")
    if "user_profile" not in st.session_state:
        st.session_state["user_profile"] = DEFAULT_PROFILE.copy()
    profile = st.session_state["user_profile"]

    degrees_text = st.text_area("Degrees (one per line)", value="\n".join(profile.get("degrees", [])), height=100)
    certs_text = st.text_area("Certifications (one per line)", value="\n".join(profile.get("certifications", [])), height=120)
    skills_text = st.text_area("Skills (one per line)", value="\n".join(profile.get("skills", [])), height=150)
    years = st.number_input("Years of Experience", min_value=0, max_value=40, value=profile.get("years_experience", 0))

    if st.button("💾 Save Profile", type="primary"):
        st.session_state["user_profile"] = {
            "degrees": [d.strip() for d in degrees_text.split("\n") if d.strip()],
            "certifications": [c.strip() for c in certs_text.split("\n") if c.strip()],
            "skills": [s.strip() for s in skills_text.split("\n") if s.strip()],
            "years_experience": years,
        }
        if "search_results" in st.session_state:
            del st.session_state["search_results"]
        st.success("Profile saved!")
