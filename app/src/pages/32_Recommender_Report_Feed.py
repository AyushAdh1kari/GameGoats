import streamlit as st

from modules.api_client import get_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("recommender")

st.title("Report Feed")
st.write("Read the current moderation queue to understand what needs curator attention.")

reports, error, _ = get_json("/reports")
if error:
    st.error(error)
    st.stop()

status_filter = st.multiselect(
    "Statuses to include",
    options=["open", "in_review", "resolved", "rejected"],
    default=["open", "in_review"],
)

filtered_reports = [report for report in reports if report["report_status"] in status_filter]

st.metric("Reports In View", len(filtered_reports))
st.dataframe(
    filtered_reports,
    use_container_width=True,
    hide_index=True,
    column_order=["report_id", "offender_type", "report_status", "report_text", "created_at"],
)
