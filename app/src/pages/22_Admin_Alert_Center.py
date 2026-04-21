import streamlit as st

from modules.api_client import delete_json, get_json, post_json, put_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("admin")

st.title("Alert Center")
st.write("Manage server alerts through the live nested alert routes.")

servers, servers_error, _ = get_json("/servers")
if servers_error:
    st.error(servers_error)
    st.stop()

selected_server = st.selectbox(
    "Select a server",
    options=servers,
    format_func=lambda server: f"#{server['server_id']} - {server['server_name']}",
)

alerts, alerts_error, _ = get_json(f"/servers/{selected_server['server_id']}/alerts")
if alerts_error:
    st.error(alerts_error)
    st.stop()

st.dataframe(
    alerts,
    use_container_width=True,
    hide_index=True,
    column_order=["alert_id", "alert_severity", "alert_type", "alert_status", "recorded_at"],
)

create_tab, update_tab, delete_tab = st.tabs(["Create Alert", "Update Alert", "Delete Alert"])

with create_tab:
    with st.form("create_alert_form"):
        severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        alert_type = st.text_input("Alert type", placeholder="latency-spike")
        alert_message = st.text_area("Alert message", placeholder="Describe the issue affecting this server.")
        create_submitted = st.form_submit_button("Create Alert", type="primary")

    if create_submitted:
        payload = {
            "alert_severity": severity,
            "alert_type": alert_type,
            "alert_message": alert_message,
        }
        response, submit_error, _ = post_json(f"/servers/{selected_server['server_id']}/alerts", payload)
        if submit_error:
            st.error(submit_error)
        else:
            st.success(f"Alert created with id {response['alert_id']}.")

with update_tab:
    if not alerts:
        st.info("No alerts are currently attached to this server.")
    else:
        selected_alert = st.selectbox(
            "Select an alert to update",
            options=alerts,
            format_func=lambda alert: f"#{alert['alert_id']} - {alert['alert_type']} [{alert['alert_status']}]",
        )
        with st.form("update_alert_form"):
            updated_severity = st.selectbox(
                "Severity",
                ["low", "medium", "high", "critical"],
                index=["low", "medium", "high", "critical"].index(selected_alert["alert_severity"]),
            )
            updated_type = st.text_input("Alert type", value=selected_alert["alert_type"])
            updated_message = st.text_area("Alert message", value=selected_alert["alert_message"])
            updated_status = st.selectbox(
                "Alert status",
                ["active", "acknowledged", "resolved"],
                index=["active", "acknowledged", "resolved"].index(selected_alert["alert_status"]),
            )
            update_submitted = st.form_submit_button("Save Alert Changes", type="primary")

        if update_submitted:
            payload = {
                "alert_id": selected_alert["alert_id"],
                "alert_severity": updated_severity,
                "alert_type": updated_type,
                "alert_message": updated_message,
                "alert_status": updated_status,
            }
            if updated_status == "acknowledged":
                payload["acknowledged_by_admin_id"] = user["id"]
            response, submit_error, _ = put_json(
                f"/servers/{selected_server['server_id']}/alerts",
                payload,
            )
            if submit_error:
                st.error(submit_error)
            else:
                st.success(response["message"])

with delete_tab:
    if not alerts:
        st.info("No alerts are available to delete.")
    else:
        alert_to_delete = st.selectbox(
            "Select an alert to delete",
            options=alerts,
            format_func=lambda alert: f"#{alert['alert_id']} - {alert['alert_type']}",
            key="alert_delete_selector",
        )
        confirm_delete = st.checkbox("I understand this will delete the selected alert.")
        if st.button("Delete Alert", type="primary", disabled=not confirm_delete):
            payload = {"alert_id": alert_to_delete["alert_id"]}
            response, delete_error, _ = delete_json(
                f"/servers/{selected_server['server_id']}/alerts",
                payload,
            )
            if delete_error:
                st.error(delete_error)
            else:
                st.success(response["message"])
