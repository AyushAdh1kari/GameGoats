import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Forum Threads", page_icon="💬")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "recommender":
    st.warning("Please log in as a Recommender from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("Forum Threads")

try:
    resp = requests.get(f"{API}/games", timeout=5)
    all_games = resp.json() if resp.status_code == 200 else []
except Exception:
    all_games = []

game_options = {g["title"]: g["game_id"] for g in all_games}
selected_title = st.selectbox("Select a game", list(game_options.keys()))
game_id = game_options.get(selected_title)

if not game_id:
    st.info("No games available.")
    st.stop()

st.divider()

try:
    threads_resp = requests.get(f"{API}/games/{game_id}/forum-threads", timeout=5)
    threads = threads_resp.json() if threads_resp.status_code == 200 else []
except Exception:
    threads = []

if not threads:
    st.info("No forum threads for this game yet.")

for thread in threads:
    with st.expander(f"📌 {thread.get('title', 'Untitled')} — User #{thread.get('created_by_user_id', '?')}"):
        st.markdown(thread.get("thread_text", ""))
        st.caption(f"Created: {thread.get('created_at', '–')}")

        thread_id = thread.get("forum_id")
        try:
            contrib_resp = requests.get(f"{API}/forum-threads/{thread_id}", timeout=5)
            contribs = contrib_resp.json() if contrib_resp.status_code == 200 else []
            if isinstance(contribs, dict):
                contribs = contribs.get("contributions", [])
        except Exception:
            contribs = []

        if contribs:
            st.markdown("---")
            for c in contribs:
                st.markdown(f"**User #{c.get('contributed_by_user_id', '?')}:** {c.get('contribution_text', '')}")
                st.caption(c.get("created_at", ""))

        st.markdown("---")
        with st.form(f"contrib_form_{thread_id}", clear_on_submit=True):
            contrib_text = st.text_area("Add to the discussion", key=f"contrib_{thread_id}", max_chars=500)
            if st.form_submit_button("Post Reply"):
                if contrib_text.strip():
                    try:
                        post_resp = requests.post(
                            f"{API}/forum-threads/{thread_id}",
                            json={
                                "contributed_by_user_id": user_id,
                                "contribution_text": contrib_text.strip(),
                            },
                            timeout=5,
                        )
                        if post_resp.status_code == 201:
                            st.success("Reply posted!")
                            st.rerun()
                        else:
                            st.error(f"Failed: {post_resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.warning("Please write something before posting.")
