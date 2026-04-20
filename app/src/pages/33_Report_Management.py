import requests
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Report Management", page_icon="📝")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "admin":
    st.warning("Please log in as an Admin from the Home page.")
    st.stop()

API = "http://web-api:4000"
admin_id = st.session_state["user_id"]

st.title("Report Management")

try:
    resp = requests.get(f"{API}/reports", timeout=5)
    reports = resp.json() if resp.status_code == 200 else []
except Exception:
    reports = []
    st.error("Could not reach the API.")

status_filter = st.selectbox("Filter by status", ["All", "open", "in_review", "resolved", "rejected"])
if status_filter != "All":
    reports = [r for r in reports if r.get("report_status") == status_filter]

st.markdown(f"**{len(reports)} reports**")

if reports:
    STATUS_COLORS = {"open": "🔵", "in_review": "🟡", "resolved": "🟢", "rejected": "🔴"}

    for r in reports:
        status = r.get("report_status", "open")
        icon = STATUS_COLORS.get(status, "⚪")
        with st.expander(
            f"{icon} Report #{r['report_id']} — {r.get('offender_type', '–')} — {status}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Created by:** User #{r.get('created_by_user_id', '–')}")
                st.markdown(f"**Offender type:** {r.get('offender_type', '–')}")
                if r.get("offender_user_id"):
                    st.markdown(f"**Offender user:** #{r['offender_user_id']}")
                if r.get("offender_reference_id"):
                    st.markdown(f"**Reference ID:** {r['offender_reference_id']}")
            with col2:
                st.markdown(f"**Status:** {status}")
                st.markdown(f"**Created:** {r.get('created_at', '–')}")
                if r.get("handled_by_admin_id"):
                    st.markdown(f"**Handled by:** Admin #{r['handled_by_admin_id']}")
                if r.get("resolved_at"):
                    st.markdown(f"**Resolved:** {r['resolved_at']}")

            st.markdown(f"**Report text:** {r.get('report_text', '–')}")
            if r.get("resolution_notes"):
                st.markdown(f"**Resolution notes:** {r['resolution_notes']}")

            st.markdown("---")
            report_id = r["report_id"]

            ac1, ac2, ac3, ac4 = st.columns(4)

            with ac1:
                if status == "open":
                    if st.button("Mark In Review", key=f"review_{report_id}", use_container_width=True):
                        try:
                            requests.put(
                                f"{API}/reports",
                                json={
                                    "report_id": report_id,
                                    "report_status": "in_review",
                                    "handled_by_admin_id": admin_id,
                                },
                                timeout=5,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with ac2:
                if status in ("open", "in_review"):
                    if st.button("Resolve", key=f"resolve_{report_id}", use_container_width=True):
                        try:
                            requests.put(
                                f"{API}/reports",
                                json={
                                    "report_id": report_id,
                                    "report_status": "resolved",
                                    "handled_by_admin_id": admin_id,
                                    "resolution_notes": "Resolved by admin.",
                                },
                                timeout=5,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with ac3:
                if status in ("open", "in_review"):
                    if st.button("Reject", key=f"reject_{report_id}", use_container_width=True):
                        try:
                            requests.put(
                                f"{API}/reports",
                                json={
                                    "report_id": report_id,
                                    "report_status": "rejected",
                                    "handled_by_admin_id": admin_id,
                                    "resolution_notes": "Rejected after investigation.",
                                },
                                timeout=5,
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with ac4:
                if st.button("Delete", key=f"del_{report_id}", use_container_width=True):
                    try:
                        requests.delete(f"{API}/reports", json={"report_id": report_id}, timeout=5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.info("No reports match the current filter.")

st.divider()

st.subheader("File a New Report")
with st.form("new_report_form", clear_on_submit=True):
    rc1, rc2 = st.columns(2)
    with rc1:
        offender_type = st.selectbox("Offender Type",
                                     ["user", "game", "comment", "thread", "server", "studio", "other"])
        offender_user_id = st.number_input("Offender User ID (optional)", min_value=0, value=0, step=1)
        offender_ref_id = st.number_input("Reference ID (optional)", min_value=0, value=0, step=1)
    with rc2:
        report_text = st.text_area("Report Description", max_chars=500)

    if st.form_submit_button("Submit Report", type="primary"):
        if report_text.strip():
            payload = {
                "created_by_user_id": admin_id,
                "offender_type": offender_type,
                "report_text": report_text.strip(),
            }
            if offender_user_id > 0:
                payload["offender_user_id"] = offender_user_id
            if offender_ref_id > 0:
                payload["offender_reference_id"] = offender_ref_id
            try:
                resp = requests.post(f"{API}/reports", json=payload, timeout=5)
                if resp.status_code == 201:
                    st.success("Report filed!")
                    st.rerun()
                else:
                    st.error(f"Failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please provide a description.")
