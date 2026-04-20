import requests
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Game Analytics", page_icon="📊")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "developer":
    st.warning("Please log in as a Developer from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("Game Analytics")

try:
    resp = requests.get(f"{API}/developers/{user_id}/games", timeout=5)
    my_games = resp.json() if resp.status_code == 200 else []
except Exception:
    my_games = []

if not my_games:
    st.info("No games found for your developer profile.")
    st.stop()

game_options = {g["title"]: g["game_id"] for g in my_games}
selected_title = st.selectbox("Select a game", list(game_options.keys()))
game_id = game_options.get(selected_title)

if not game_id:
    st.stop()

game = next((g for g in my_games if g["game_id"] == game_id), {})

col1, col2, col3, col4 = st.columns(4)
rating = game.get("average_rating", 0)
if isinstance(rating, str):
    rating = float(rating)
col1.metric("Average Rating", f"⭐ {rating:.2f}")
col2.metric("Platform", game.get("platform", "–"))
col3.metric("Status", game.get("lifecycle_status", "–"))
col4.metric("Release Year", game.get("release_year", "–"))

st.divider()

st.subheader("Rating Trends")
try:
    trends_resp = requests.get(f"{API}/games/{game_id}/ratings/trends", timeout=5)
    trends = trends_resp.json() if trends_resp.status_code == 200 else []
except Exception:
    trends = []

if trends:
    df = pd.DataFrame(trends)
    if "date" in df.columns and "average_rating" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
        st.line_chart(df["average_rating"])
    else:
        st.info("Trend data format not recognized.")
else:
    try:
        comments_resp = requests.get(f"{API}/games/{game_id}/comments", timeout=5)
        comments = comments_resp.json() if comments_resp.status_code == 200 else []
    except Exception:
        comments = []

    if comments:
        df = pd.DataFrame(comments)
        if "created_at" in df.columns and "rating" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"])
            df = df.sort_values("created_at")
            df["rolling_avg"] = df["rating"].expanding().mean()
            chart_df = df.set_index("created_at")[["rating", "rolling_avg"]]
            st.line_chart(chart_df)
            st.caption("Rating per review with cumulative average")
        else:
            st.info("No rating data available to chart.")
    else:
        st.info("No reviews yet for this game — ratings chart will appear after reviews are submitted.")

st.divider()

st.subheader("Recent Reviews")
try:
    comments_resp = requests.get(f"{API}/games/{game_id}/comments", timeout=5)
    comments = comments_resp.json() if comments_resp.status_code == 200 else []
except Exception:
    comments = []

if comments:
    for c in comments[:10]:
        with st.container(border=True):
            stars = "⭐" * int(c.get("rating", 0))
            st.markdown(f"**User #{c.get('created_by_user_id', '?')}** {stars}")
            st.write(c.get("comment_text", ""))
else:
    st.info("No reviews yet.")
