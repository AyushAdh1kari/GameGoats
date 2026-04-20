import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Studio Management", page_icon="🏢")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "developer":
    st.warning("Please log in as a Developer from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("Studio Management")

try:
    studios_resp = requests.get(f"{API}/developers/{user_id}/studios", timeout=5)
    studios = studios_resp.json() if studios_resp.status_code == 200 else []
except Exception:
    studios = []

if not studios:
    st.info("No studio memberships found for your profile.")
    st.stop()

studio_options = {s.get("studio_name", f"Studio #{s['studio_id']}"): s for s in studios}
selected_name = st.selectbox("Select a studio", list(studio_options.keys()))
studio = studio_options[selected_name]
studio_id = studio["studio_id"]

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Studio Details")
    st.markdown(f"**Name:** {studio.get('studio_name', '–')}")
    st.markdown(f"**Region:** {studio.get('headquarters_region', '–')}")
    st.markdown(f"**Created:** {str(studio.get('created_at', '–'))[:10]}")

with col2:
    st.subheader("Edit Studio")
    with st.form("edit_studio_form"):
        new_name = st.text_input("Studio Name", value=studio.get("studio_name", ""), max_chars=120)
        regions = ["NA-East", "NA-West", "EU-Central", "EU-West", "AP-South", "LATAM"]
        current_region = studio.get("headquarters_region", regions[0])
        region_idx = regions.index(current_region) if current_region in regions else 0
        new_region = st.selectbox("Region", regions, index=region_idx)
        if st.form_submit_button("Update Studio", type="primary"):
            try:
                resp = requests.put(
                    f"{API}/studios/{studio_id}",
                    json={"studio_name": new_name.strip(), "headquarters_region": new_region},
                    timeout=5,
                )
                if resp.status_code == 200:
                    st.success("Studio updated!")
                    st.rerun()
                else:
                    st.error(f"Failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("Studio Games")
try:
    games_resp = requests.get(f"{API}/studios/{studio_id}/games", timeout=5)
    games = games_resp.json() if games_resp.status_code == 200 else []
except Exception:
    games = []

if games:
    st.dataframe(
        [
            {
                "Title": g.get("title", "–"),
                "Genre": g.get("genre", "–"),
                "Platform": g.get("platform", "–"),
                "Rating": g.get("average_rating", "–"),
                "Status": g.get("lifecycle_status", "–"),
            }
            for g in games
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No games published by this studio yet.")
