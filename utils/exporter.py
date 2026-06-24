"""
exporter.py — Export job results to Excel with formatted worksheets.
"""

import io
import pandas as pd
from datetime import datetime


def jobs_to_dataframe(jobs: list[dict]) -> pd.DataFrame:
    """Convert job list to a clean DataFrame for display and export."""
    if not jobs:
        return pd.DataFrame()

    display_cols = [
        "company", "title", "location", "salary",
        "education_required", "certifications_required", "skills_required",
        "match_status", "match_score", "link", "date_posted",
    ]

    df = pd.DataFrame(jobs)
    # Only keep columns that exist
    cols = [c for c in display_cols if c in df.columns]
    df = df[cols].copy()

    # Rename for display
    df.columns = [c.replace("_", " ").title() for c in df.columns]
    return df


def export_to_excel(jobs: list[dict]) -> bytes:
    """
    Create a multi-sheet Excel file:
    - Sheet 1: All jobs with match results
    - Sheet 2: Yes matches only
    - Sheet 3: Partial matches only
    - Sheet 4: Summary stats
    Returns bytes suitable for st.download_button.
    """
    df_all = jobs_to_dataframe(jobs)
    if df_all.empty:
        return b""

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Sheet 1: All results
        df_all.to_excel(writer, sheet_name="All Jobs", index=False)

        # Sheet 2 & 3: Filtered
        if "Match Status" in df_all.columns:
            df_yes = df_all[df_all["Match Status"].str.contains("Yes", na=False)]
            df_partial = df_all[df_all["Match Status"].str.contains("Partial", na=False)]
            df_yes.to_excel(writer, sheet_name="Qualified Jobs", index=False)
            df_partial.to_excel(writer, sheet_name="Partial Matches", index=False)

        # Sheet 4: Summary
        summary = _build_summary(df_all)
        summary.to_excel(writer, sheet_name="Summary", index=False)

        # Auto-width columns
        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            for col in ws.columns:
                max_len = max(
                    (len(str(cell.value)) for cell in col if cell.value), default=10
                )
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 50)

    return output.getvalue()


def _build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Build a summary stats DataFrame."""
    total = len(df)
    status_col = "Match Status"
    if status_col not in df.columns:
        return pd.DataFrame({"Metric": ["Total Jobs"], "Value": [total]})

    yes = df[status_col].str.contains("Yes", na=False).sum()
    partial = df[status_col].str.contains("Partial", na=False).sum()
    no = df[status_col].str.contains("No", na=False).sum()

    avg_score = df["Match Score"].mean() if "Match Score" in df.columns else 0

    summary_data = {
        "Metric": [
            "Total Jobs Found",
            "Fully Qualified (Yes)",
            "Partially Qualified",
            "Not Qualified",
            "Average Match Score",
            "Export Date",
        ],
        "Value": [
            total,
            yes,
            partial,
            no,
            f"{avg_score:.1f}%",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        ],
    }
    return pd.DataFrame(summary_data)
