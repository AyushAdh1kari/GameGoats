import streamlit as st

from modules.api_client import get_json, post_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("player")

st.title("Submit Safety Report")
st.write("Players can escalate issues through the live `POST /reports` endpoint.")

games, _, _ = get_json("/games")
reports, reports_error, _ = get_json("/reports")

with st.form("player_report_form"):
    offender_type = st.selectbox(
        "Offender type",
        options=["user", "game", "comment", "thread", "server", "studio", "other"],
    )
    offender_reference_id = st.number_input("Reference id", min_value=0, step=1, value=0)
    offender_user_id = st.number_input("Offender user id (optional)", min_value=0, step=1, value=0)
    if games:
        selected_game = st.selectbox(
            "Related game (optional context)",
            options=[None] + games,
            format_func=lambda game: "None" if game is None else f"#{game['game_id']} - {game['title']}",
        )
    else:
        selected_game = None
    report_text = st.text_area("Report details", placeholder="Describe what happened and why it should be reviewed.")
    submitted = st.form_submit_button("Submit Report", type="primary")

if submitted:
    payload = {
        "created_by_user_id": user["id"],
        "offender_type": offender_type,
        "report_text": report_text,
    }
    if offender_reference_id > 0:
        payload["offender_reference_id"] = offender_reference_id
    elif selected_game is not None:
        payload["offender_reference_id"] = selected_game["game_id"]
    if offender_user_id > 0:
        payload["offender_user_id"] = offender_user_id

    if not report_text.strip():
        st.error("Report text is required.")
    else:
        response, submit_error, _ = post_json("/reports", payload)
        if submit_error:
            st.error(submit_error)
        else:
            st.success(f"Report submitted successfully with id {response['report_id']}.")

st.subheader("Recent Reports")
if reports_error:
    st.error(reports_error)
else:
    st.dataframe(
        reports[:10],
        use_container_width=True,
        hide_index=True,
        column_order=["report_id", "offender_type", "report_status", "created_by_user_id", "created_at"],
    )
