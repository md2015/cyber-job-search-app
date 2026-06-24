"""
export_page.py — Export results to Excel and view as table.
"""

import streamlit as st
import pandas as pd
from utils.exporter import jobs_to_dataframe, export_to_excel


def render():
    st.title("📥 Export Results")

    results = st.session_state.get("search_results", [])

    if not results:
        st.info("No search results yet. Run a job search first.")
        return

    df = jobs_to_dataframe(results)

    st.markdown(f"**{len(results)} jobs** ready to export.")
    st.markdown("---")

    # ── Full table ────────────────────────────────────────────────────────────
    st.subheader("📋 Full Results Table")

    # Color-code the Match Status column
    def color_status(val):
        if "Yes" in str(val):
            return "background-color: #d4edda; color: #155724"
        elif "Partial" in str(val):
            return "background-color: #fff3cd; color: #856404"
        elif "No" in str(val):
            return "background-color: #f8d7da; color: #721c24"
        return ""

    if "Match Status" in df.columns:
        styled = df.style.applymap(color_status, subset=["Match Status"])
        st.dataframe(styled, use_container_width=True, height=400)
    else:
        st.dataframe(df, use_container_width=True, height=400)

    st.markdown("---")

    # ── Download buttons ─────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        excel_bytes = export_to_excel(results)
        if excel_bytes:
            st.download_button(
                label="⬇️ Download Full Excel Report",
                data=excel_bytes,
                file_name="cyberjobs_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True,
            )
            st.caption("Includes: All Jobs, Qualified Jobs, Partial Matches, Summary tabs.")

    with col2:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_bytes,
            file_name="cyberjobs_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")

    # ── Filtered views ────────────────────────────────────────────────────────
    st.subheader("🔍 Filtered Views")
    tab1, tab2, tab3 = st.tabs(["✅ Qualified", "⚠️ Partial Match", "❌ Not Qualified"])

    if "Match Status" in df.columns:
        with tab1:
            yes_df = df[df["Match Status"].str.contains("Yes", na=False)]
            st.markdown(f"**{len(yes_df)} jobs** where you fully qualify.")
            st.dataframe(yes_df, use_container_width=True)

        with tab2:
            partial_df = df[df["Match Status"].str.contains("Partial", na=False)]
            st.markdown(f"**{len(partial_df)} jobs** where you partially qualify.")
            st.dataframe(partial_df, use_container_width=True)

        with tab3:
            no_df = df[df["Match Status"].str.contains("No", na=False)]
            st.markdown(f"**{len(no_df)} jobs** where you currently don't qualify.")
            st.dataframe(no_df, use_container_width=True)
