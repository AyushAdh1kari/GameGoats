import streamlit as st

from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("admin")

st.title("Richard Admin Home")
st.write(
    f"Welcome, {user['display_name']}. This operations workspace covers the live servers, alerts, and reports endpoints."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Server Dashboard")
    st.caption("Inspect server health and drill into one environment at a time.")
    if st.button("Open Server Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/21_Admin_Server_Dashboard.py")

with col2:
    st.subheader("Alert Center")
    st.caption("Create, update, and resolve alert records tied to a server.")
    if st.button("Open Alert Center", type="primary", use_container_width=True):
        st.switch_page("pages/22_Admin_Alert_Center.py")

with col3:
    st.subheader("Report Console")
    st.caption("Review incoming reports and move them through moderation status.")
    if st.button("Open Report Console", type="primary", use_container_width=True):
        st.switch_page("pages/23_Admin_Report_Console.py")

st.divider()
st.markdown(
    """
    ### Admin demo flow
    1. Review `GET /servers` and `GET /servers/<server_id>`.
    2. Manage alert records under `GET/POST/PUT/DELETE /servers/<server_id>/alerts`.
    3. Review and update incidents through the `reports` API.
    """
)
