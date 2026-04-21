import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Recommendation Feed", page_icon="🎯")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "recommender":
    st.warning("Please log in as a Recommender from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("Recommendation Feed")

try:
    resp = requests.get(f"{API}/users/{user_id}/recommendations", timeout=5)
    recs = resp.json() if resp.status_code == 200 else []
except Exception:
    recs = []
    st.error("Could not load recommendations.")

if not recs:
    st.info("No recommendations in your queue.")
    st.stop()

if "rec_index" not in st.session_state:
    st.session_state["rec_index"] = 0

idx = st.session_state["rec_index"] % len(recs)
rec = recs[idx]

st.caption(f"Recommendation {idx + 1} of {len(recs)}")

with st.container(border=True):
    game_id = rec.get("game_id")
    try:
        game_resp = requests.get(f"{API}/games/{game_id}", timeout=5)
        game = game_resp.json() if game_resp.status_code == 200 else {}
    except Exception:
        game = {}

    st.markdown(f"## {game.get('title', f'Game #{game_id}')}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Genre:** {game.get('genre', '–')}")
        st.markdown(f"**Platform:** {game.get('platform', '–')}")
        rating = game.get("average_rating", 0)
        if isinstance(rating, str):
            rating = float(rating)
        st.markdown(f"**Rating:** ⭐ {rating:.1f}")
    with col2:
        score = rec.get("match_score", 0)
        if isinstance(score, str):
            score = float(score)
        st.metric("Match Score", f"{score:.0f}%")
        st.markdown(f"**Status:** {rec.get('recommendation_status', '–')}")

    st.markdown(f"**Why this game?** {rec.get('recommendation_reason', '–')}")

    if game.get("description"):
        st.markdown(game["description"])

st.write("")

col_prev, col_accept, col_dismiss, col_save, col_next = st.columns(5)

with col_prev:
    if st.button("← Previous", use_container_width=True):
        st.session_state["rec_index"] = (idx - 1) % len(recs)
        st.rerun()

with col_accept:
    if st.button("Accept", type="primary", use_container_width=True):
        try:
            requests.put(
                f"{API}/users/{user_id}/recommendations/{rec['recommendation_id']}",
                json={"recommendation_status": "accepted"},
                timeout=5,
            )
            st.success("Accepted!")
            st.session_state["rec_index"] = (idx + 1) % len(recs)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with col_dismiss:
    if st.button("Dismiss", use_container_width=True):
        try:
            requests.put(
                f"{API}/users/{user_id}/recommendations/{rec['recommendation_id']}",
                json={"recommendation_status": "dismissed"},
                timeout=5,
            )
            st.info("Dismissed.")
            st.session_state["rec_index"] = (idx + 1) % len(recs)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with col_save:
    if st.button("Save for Later", use_container_width=True):
        try:
            requests.put(
                f"{API}/users/{user_id}/recommendations/{rec['recommendation_id']}",
                json={"is_saved": True},
                timeout=5,
            )
            st.success("Saved!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with col_next:
    if st.button("Next →", use_container_width=True):
        st.session_state["rec_index"] = (idx + 1) % len(recs)
        st.rerun()
