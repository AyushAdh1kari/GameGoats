import requests
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Alert Management", page_icon="🚨")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "admin":
    st.warning("Please log in as an Admin from the Home page.")
    st.stop()

API = "http://web-api:4000"
admin_id = st.session_state["user_id"]

st.title("Alert Management")

try:
    servers_resp = requests.get(f"{API}/servers", timeout=5)
    servers = servers_resp.json() if servers_resp.status_code == 200 else []
except Exception:
    servers = []

server_options = {s["server_name"]: s["server_id"] for s in servers}
selected_server = st.selectbox("Select a server", list(server_options.keys()))
server_id = server_options.get(selected_server)

if not server_id:
    st.info("No servers available.")
    st.stop()

st.divider()

try:
    alerts_resp = requests.get(f"{API}/servers/{server_id}/alerts", timeout=5)
    alerts = alerts_resp.json() if alerts_resp.status_code == 200 else []
except Exception:
    alerts = []

SEVERITY_ICONS = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

if alerts:
    st.subheader(f"Alerts for {selected_server}")

    active = sum(1 for a in alerts if a.get("alert_status") == "active")
    acked = sum(1 for a in alerts if a.get("alert_status") == "acknowledged")
    resolved = sum(1 for a in alerts if a.get("alert_status") == "resolved")

    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Active", active)
    mc2.metric("Acknowledged", acked)
    mc3.metric("Resolved", resolved)

    for a in alerts:
        sev = a.get("alert_severity", "low")
        icon = SEVERITY_ICONS.get(sev, "⚪")
        with st.expander(f"{icon} [{sev.upper()}] {a.get('alert_type', '–')} — {a.get('alert_status', '–')}"):
            st.markdown(f"**Message:** {a.get('alert_message', '–')}")
            st.caption(f"Recorded: {a.get('recorded_at', '–')}")

            if a.get("acknowledged_at"):
                st.caption(f"Acknowledged: {a.get('acknowledged_at')} by Admin #{a.get('acknowledged_by_admin_id')}")
            if a.get("resolved_at"):
                st.caption(f"Resolved: {a.get('resolved_at')}")

            ac1, ac2, ac3 = st.columns(3)
            alert_id = a["alert_id"]

            with ac1:
                if a.get("alert_status") == "active":
                    if st.button("Acknowledge", key=f"ack_{alert_id}", use_container_width=True):
                        try:
                            requests.put(
                                f"{API}/servers/{server_id}/alerts",
                                json={
                                    "alert_id": alert_id,
                                    "alert_status": "acknowledged",
                                    "acknowledged_by_admin_id": admin_id,
                                },
                                timeout=5,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with ac2:
                if a.get("alert_status") in ("active", "acknowledged"):
                    if st.button("Resolve", key=f"res_{alert_id}", use_container_width=True):
                        try:
                            requests.put(
                                f"{API}/servers/{server_id}/alerts",
                                json={"alert_id": alert_id, "alert_status": "resolved"},
                                timeout=5,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with ac3:
                if st.button("Delete", key=f"del_{alert_id}", use_container_width=True):
                    try:
                        requests.delete(
                            f"{API}/servers/{server_id}/alerts",
                            json={"alert_id": alert_id},
                            timeout=5,
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.info("No alerts for this server.")

st.divider()

st.subheader("Create Alert")
with st.form("new_alert_form", clear_on_submit=True):
    nc1, nc2 = st.columns(2)
    with nc1:
        alert_severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
        alert_type = st.text_input("Alert Type", max_chars=80, placeholder="e.g. latency-spike")
    with nc2:
        alert_message = st.text_area("Message", max_chars=255, placeholder="Describe the alert...")
    if st.form_submit_button("Create Alert", type="primary"):
        if alert_type.strip() and alert_message.strip():
            try:
                resp = requests.post(
                    f"{API}/servers/{server_id}/alerts",
                    json={
                        "alert_severity": alert_severity,
                        "alert_type": alert_type.strip(),
                        "alert_message": alert_message.strip(),
                    },
                    timeout=5,
                )
                if resp.status_code == 201:
                    st.success("Alert created!")
                    st.rerun()
                else:
                    st.error(f"Failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill in both type and message.")
