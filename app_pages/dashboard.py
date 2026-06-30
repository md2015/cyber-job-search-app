"""
dashboard.py — Analytics dashboard with Plotly charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.exporter import jobs_to_dataframe


def render():
    st.title("📊 Job Intelligence Dashboard")

    results = st.session_state.get("search_results", [])

    if not results:
        st.info("Run a job search first to see your dashboard.")
        _render_placeholder_charts()
        return

    df = pd.DataFrame(results)

    # ── KPI row ─────────────────────────────────────────────────────────────
    total = len(df)
    yes_count = df["match_status"].str.contains("Yes", na=False).sum()
    partial_count = df["match_status"].str.contains("Partial", na=False).sum()
    no_count = df["match_status"].str.contains("No", na=False).sum()
    avg_score = df["match_score"].mean() if "match_score" in df.columns else 0

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Jobs", total)
    k2.metric("✅ Qualified", yes_count)
    k3.metric("⚠️ Partial", partial_count)
    k4.metric("❌ Not Qualified", no_count)
    k5.metric("Avg Match Score", f"{avg_score:.0f}%")

    st.markdown("---")

    # ── Row 1: Match distribution + Score histogram ──────────────────────
    c1, c2 = st.columns(2)

    with c1:
        status_counts = df["match_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        # Clean status labels for display
        status_counts["Status"] = status_counts["Status"].str.replace(
            r"[✅⚠️❌]\s*", "", regex=True
        )
        fig_pie = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Qualification Distribution",
            color="Status",
            color_discrete_map={
                "Yes": "#2ecc71",
                "Partial Match": "#f39c12",
                "No": "#e74c3c",
            },
            hole=0.4,
        )
        fig_pie.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        fig_hist = px.histogram(
            df,
            x="match_score",
            nbins=20,
            title="Match Score Distribution",
            labels={"match_score": "Match Score (%)"},
            color_discrete_sequence=["#3498db"],
        )
        fig_hist.add_vline(
            x=75, line_dash="dash", line_color="#2ecc71",
            annotation_text="Qualified threshold"
        )
        fig_hist.add_vline(
            x=45, line_dash="dash", line_color="#f39c12",
            annotation_text="Partial threshold"
        )
        fig_hist.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Row 2: Jobs by company + Score by company ────────────────────────
    c3, c4 = st.columns(2)

    with c3:
        company_counts = df["company"].value_counts().reset_index()
        company_counts.columns = ["Company", "Job Count"]
        fig_bar = px.bar(
            company_counts.head(15),
            x="Job Count",
            y="Company",
            orientation="h",
            title="Jobs by Company (Top 15)",
            color="Job Count",
            color_continuous_scale="Blues",
        )
        fig_bar.update_layout(
            yaxis={"categoryorder": "total ascending"},
            margin=dict(t=40, b=10, l=10, r=10),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        avg_by_company = (
            df.groupby("company")["match_score"].mean().reset_index()
        )
        avg_by_company.columns = ["Company", "Avg Match Score"]
        avg_by_company = avg_by_company.sort_values("Avg Match Score", ascending=True)
        fig_score = px.bar(
            avg_by_company.tail(15),
            x="Avg Match Score",
            y="Company",
            orientation="h",
            title="Average Match Score by Company",
            color="Avg Match Score",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
        )
        fig_score.update_layout(
            yaxis={"categoryorder": "total ascending"},
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_score, use_container_width=True)

    # ── Row 3: Remote vs On-site + Score component breakdown ────────────
    c5, c6 = st.columns(2)

    with c5:
        if "is_remote" in df.columns:
            remote_counts = df["is_remote"].map(
                {True: "Remote", False: "On-site"}
            ).value_counts().reset_index()
            remote_counts.columns = ["Type", "Count"]
            fig_remote = px.pie(
                remote_counts,
                names="Type",
                values="Count",
                title="Remote vs On-site",
                color_discrete_sequence=["#9b59b6", "#3498db"],
                hole=0.4,
            )
            fig_remote.update_layout(margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_remote, use_container_width=True)

    with c6:
        # Score component radar (for top 10 jobs)
        if all(c in df.columns for c in ["degree_score", "cert_score", "skill_score"]):
            top_jobs = df.nlargest(10, "match_score")
            fig_scatter = px.scatter(
                df,
                x="cert_score",
                y="skill_score",
                size="degree_score",
                color="match_score",
                hover_data=["company", "title"],
                title="Score Components (Cert vs Skill, size = Degree)",
                color_continuous_scale="RdYlGn",
                range_color=[0, 100],
                labels={
                    "cert_score": "Cert Score (%)",
                    "skill_score": "Skill Score (%)",
                    "match_score": "Total Score",
                },
            )
            fig_scatter.update_layout(margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ── Skills gap analysis ──────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 Skills Gap Analysis")

    if "match_detail" in df.columns:
        all_missing = []
        for row in results:
            detail = row.get("match_detail", {})
            certs_detail = detail.get("certs", "")
            if "Missing:" in certs_detail:
                missing_part = certs_detail.split("Missing:")[-1].strip()
                for item in missing_part.split(","):
                    item = item.strip().strip(".")
                    if item:
                        all_missing.append(item)

        if all_missing:
            from collections import Counter
            missing_counts = Counter(all_missing).most_common(10)
            gap_df = pd.DataFrame(missing_counts, columns=["Missing Cert/Skill", "Frequency"])
            fig_gap = px.bar(
                gap_df,
                x="Frequency",
                y="Missing Cert/Skill",
                orientation="h",
                title="Most Frequently Missing Certifications",
                color="Frequency",
                color_continuous_scale="Reds",
            )
            fig_gap.update_layout(
                yaxis={"categoryorder": "total ascending"},
                margin=dict(t=40, b=10, l=10, r=10),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_gap, use_container_width=True)
            st.caption(
                "These are the certifications most often required by jobs you partially or don't qualify for."
            )
        else:
            st.success("No major certification gaps found in current results.")


def _render_placeholder_charts():
    """Show sample chart layout before any search is run."""
    st.markdown("### Sample Dashboard Preview")
    import numpy as np
    sample = pd.DataFrame({
        "Status": ["Qualified", "Partial Match", "Not Qualified"],
        "Count": [45, 30, 25],
    })
    fig = px.pie(
        sample, names="Status", values="Count",
        title="Example: Qualification Distribution",
        color="Status",
        color_discrete_map={
            "Qualified": "#2ecc71",
            "Partial Match": "#f39c12",
            "Not Qualified": "#e74c3c",
        },
        hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Run a job search to populate this dashboard with real data.")
