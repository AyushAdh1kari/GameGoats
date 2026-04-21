import streamlit as st

from modules.api_client import get_json, post_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("recommender")

st.title("Safety Escalation")
st.write("Recommenders can flag suspicious titles or behavior through `POST /reports`.")

games, _, _ = get_json("/games")

with st.form("recommender_report_form"):
    report_scope = st.selectbox("Report scope", ["game", "user", "comment", "thread", "server", "studio", "other"])
    selected_game = st.selectbox(
        "Related game",
        options=[None] + games,
        format_func=lambda game: "None" if game is None else f"#{game['game_id']} - {game['title']}",
    )
    offender_reference_id = st.number_input("Reference id override", min_value=0, step=1, value=0)
    report_text = st.text_area("Report details")
    submitted = st.form_submit_button("Send Escalation", type="primary")

if submitted:
    payload = {
        "created_by_user_id": user["id"],
        "offender_type": report_scope,
        "report_text": report_text,
    }
    if offender_reference_id > 0:
        payload["offender_reference_id"] = offender_reference_id
    elif selected_game is not None:
        payload["offender_reference_id"] = selected_game["game_id"]

    response, submit_error, _ = post_json("/reports", payload)
    if submit_error:
        st.error(submit_error)
    else:
        st.success(f"Escalation sent successfully with report id {response['report_id']}.")
