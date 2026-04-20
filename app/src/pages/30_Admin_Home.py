import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Admin Home", page_icon="🔧")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "admin":
    st.warning("Please log in as an Admin from the Home page.")
    st.stop()

API = "http://web-api:4000"
username = st.session_state["username"]

st.title(f"Welcome, {username}!")
st.markdown("System administration dashboard — servers, alerts, and reports.")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        resp = requests.get(f"{API}/servers", timeout=5)
        servers = resp.json() if resp.status_code == 200 else []
        healthy = sum(1 for s in servers if s.get("status") == "healthy")
        total = len(servers)
    except Exception:
        healthy, total = "–", "–"
    st.metric("Servers", f"{healthy} / {total} healthy")

with col2:
    try:
        resp = requests.get(f"{API}/reports", timeout=5)
        reports = resp.json() if resp.status_code == 200 else []
        open_count = sum(1 for r in reports if r.get("report_status") == "open")
    except Exception:
        open_count = "–"
    st.metric("Open Reports", open_count)

with col3:
    down_count = sum(1 for s in servers if s.get("status") == "down") if isinstance(servers, list) else "–"
    st.metric("Servers Down", down_count)

st.divider()

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("Server Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/31_Server_Dashboard.py")

with col_b:
    if st.button("Alert Management", use_container_width=True):
        st.switch_page("pages/32_Alert_Management.py")

with col_c:
    if st.button("Report Management", use_container_width=True):
        st.switch_page("pages/33_Report_Management.py")
