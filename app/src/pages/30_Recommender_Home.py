import streamlit as st

from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("recommender")

st.title("Alex Recommender Home")
st.write(
    f"Welcome, {user['display_name']}. This workspace uses the currently live APIs for catalog curation and community safety escalation."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Catalog Watch")
    st.caption("Track the current game catalog and spot titles worth surfacing to players.")
    if st.button("Open Catalog Watch", type="primary", use_container_width=True):
        st.switch_page("pages/31_Recommender_Catalog.py")

with col2:
    st.subheader("Report Feed")
    st.caption("Scan recent moderation issues to understand what is trending in the community.")
    if st.button("Open Report Feed", type="primary", use_container_width=True):
        st.switch_page("pages/32_Recommender_Report_Feed.py")

with col3:
    st.subheader("Safety Escalation")
    st.caption("Submit a new issue when a title or player should be reviewed.")
    if st.button("Open Safety Form", type="primary", use_container_width=True):
        st.switch_page("pages/33_Recommender_Submit_Report.py")
