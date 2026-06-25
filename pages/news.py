import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Set page settings
st.set_page_config(page_title="World Cup 2026 Feed Tracker", layout="wide", page_icon="⚽")
st.title("🏆 FIFA World Cup 2026 — Live Feed Hub")


# Mock function simulating World Cup API calls for live text / scores
# Replace the URL with a real sports API endpoint during active tournament matchdays
def get_world_cup_live_data():
    # Example structure representing real-time API return payloads
    return [
        {
            "match": "Group A: United States vs. Mexico",
            "status": "LIVE - 64'",
            "score": "2 - 1",
            "latest_event": "⚽ Goal! Christian Pulisic finds the bottom corner (61').",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        },
        {
            "match": "Group B: Canada vs. England",
            "status": "LIVE - 12'",
            "score": "0 - 0",
            "latest_event": "🟨 Yellow Card: Alphonso Davies (9').",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        },
        {
            "match": "Group C: Argentina vs. France",
            "status": "UPCOMING",
            "score": "04:00 PM",
            "latest_event": "Teams are arriving at the stadium.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    ]


# RSS Media Feed Fetcher for Latest News
def get_world_cup_news():
    # Feeds can be sourced from major outlets like Sky Sports, ESPN or BBC Sports soccer links
    import feedparser
    feed_url = "https://espn.com"
    parsed = feedparser.parse(feed_url)
    return parsed.entries[:5]


# Layout: Split dashboard into Live Scores and Tournament News
col_scores, col_news = st.columns([3, 2])


# --- FRAGMENT 1: AUTO-REFRESHING MATCH FEED ---
@st.fragment(run_every=15)  # Refreshes live match timelines every 15 seconds
def render_live_scores():
    with col_scores:
        st.subheader("⏱️ Live Match Tracker")
        st.caption("Auto-refreshing every 15 seconds")
        matches = get_world_cup_live_data()
        for match in matches:
            # Highlight live matches using UI styling cards
            is_live = "LIVE" in match["status"]
            border_color = "red" if is_live else "gray"
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {match['match']}")
                    st.markdown(f"**Latest Activity:** {match['latest_event']}")
                with col2:
                    if is_live:
                        st.error(f"● {match['status']}")
                        st.subheader(f"` {match['score']} `")
                    else:
                        st.info(match['status'])
                        st.caption(f"Kickoff: {match['score']}")
                st.caption(f"Last updated feed packet at: {match['timestamp']}")


# --- FRAGMENT 2: AUTO-REFRESHING TOURNAMENT NEWS ---
@st.fragment(run_every=180)  # Refreshes editorial news every 3 minutes
def render_news_feed():
    with col_news:
        st.subheader("📰 Latest World Cup News")
        st.caption("Auto-refreshing every 3 minutes")
        try:
            articles = get_world_cup_news()
            for article in articles:
                with st.container(border=True):
                    st.markdown(f"#### [{article.title}]({article.link})")
                    st.write(article.get("summary", "Click link to view story details."))
                    if "published" in article:
                        st.caption(f"📅 {article.published}")
        except Exception as e:
            st.error("Could not load the latest news items right now.")


# Execute independent fragments side-by-side
render_live_scores()
render_news_feed()