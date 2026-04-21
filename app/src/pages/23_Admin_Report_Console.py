import streamlit as st

from modules.api_client import delete_json, get_json, post_json, put_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("admin")

st.title("Report Console")
st.write("Review and act on the live `reports` resource.")

reports, error, _ = get_json("/reports")
if error:
    st.error(error)
    st.stop()

status_filter = st.selectbox("Filter by status", ["All", "open", "in_review", "resolved", "rejected"])
type_filter = st.selectbox("Filter by offender type", ["All", "user", "game", "comment", "thread", "server", "studio", "other"])

filtered_reports = []
for report in reports:
    status_match = status_filter == "All" or report["report_status"] == status_filter
    type_match = type_filter == "All" or report["offender_type"] == type_filter
    if status_match and type_match:
        filtered_reports.append(report)

st.dataframe(
    filtered_reports,
    use_container_width=True,
    hide_index=True,
    column_order=["report_id", "offender_type", "report_status", "created_by_user_id", "created_at"],
)

create_tab, update_tab, delete_tab = st.tabs(["Create Report", "Update Report", "Delete Report"])

with create_tab:
    with st.form("create_report_form"):
        offender_type = st.selectbox(
            "Offender type",
            ["user", "game", "comment", "thread", "server", "studio", "other"],
        )
        offender_reference_id = st.number_input("Reference id", min_value=0, step=1, value=0)
        offender_user_id = st.number_input("Offender user id", min_value=0, step=1, value=0)
        report_text = st.text_area("Report text", placeholder="Describe the violation or incident.")
        create_submitted = st.form_submit_button("Create Report", type="primary")

    if create_submitted:
        payload = {
            "created_by_user_id": user["id"],
            "offender_type": offender_type,
            "report_text": report_text,
        }
        if offender_reference_id > 0:
            payload["offender_reference_id"] = offender_reference_id
        if offender_user_id > 0:
            payload["offender_user_id"] = offender_user_id
        response, submit_error, _ = post_json("/reports", payload)
        if submit_error:
            st.error(submit_error)
        else:
            st.success(f"Report created with id {response['report_id']}.")

with update_tab:
    if not reports:
        st.info("No reports are available to update.")
    else:
        selected_report = st.selectbox(
            "Select a report to update",
            options=reports,
            format_func=lambda report: f"#{report['report_id']} - {report['offender_type']} [{report['report_status']}]",
        )
        status_options = ["open", "in_review", "resolved", "rejected"]
        with st.form("update_report_form"):
            report_status = st.selectbox(
                "Report status",
                status_options,
                index=status_options.index(selected_report["report_status"]),
            )
            resolution_notes = st.text_area(
                "Resolution notes",
                value=selected_report["resolution_notes"] or "",
            )
            update_submitted = st.form_submit_button("Save Report Changes", type="primary")

        if update_submitted:
            payload = {
                "report_id": selected_report["report_id"],
                "report_status": report_status,
                "handled_by_admin_id": user["id"],
                "resolution_notes": resolution_notes,
            }
            response, submit_error, _ = put_json("/reports", payload)
            if submit_error:
                st.error(submit_error)
            else:
                st.success(response["message"])

with delete_tab:
    if not reports:
        st.info("No reports are available to delete.")
    else:
        report_to_delete = st.selectbox(
            "Select a report to delete",
            options=reports,
            format_func=lambda report: f"#{report['report_id']} - {report['offender_type']}",
            key="report_delete_selector",
        )
        confirm_delete = st.checkbox("I understand this will permanently delete the report record.")
        if st.button("Delete Report", type="primary", disabled=not confirm_delete):
            response, delete_error, _ = delete_json("/reports", {"report_id": report_to_delete["report_id"]})
            if delete_error:
                st.error(delete_error)
            else:
                st.success(response["message"])
