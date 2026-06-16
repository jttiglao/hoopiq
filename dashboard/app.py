import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ── Config ───────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "player_stats.csv")

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=0)
def load_data():
    if not os.path.exists(DATA_PATH):
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        from etl.pipeline import run_pipeline
        run_pipeline()
    df = pd.read_csv(DATA_PATH)
    return df
# ── App ──────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="HoopIQ", layout="wide")
st.title("🏀 NBA Analytics Dashboard")
st.caption(f"Season: 2025-26 | Data via nba_api")

# ── About Section ─────────────────────────────────────────────────────────────
with st.expander("ℹ️ About HoopIQ", expanded=False):
    st.markdown("""
    **HoopIQ** is an end-to-end NBA analytics platform built to demonstrate 
    enterprise-grade data engineering and AI-assisted reporting.
    
    **How it works:**
    - 🔄 **ETL Pipeline** — Pulls live player stats from the official NBA Stats API, 
    cleans and normalizes the data, and exports a master dataset
    - 📊 **Interactive Dashboard** — Filter by team, games played, and performance 
    tier to explore player stats dynamically
    - ⏱️ **Automated Refresh** — A scheduler runs the pipeline daily at 6am to keep 
    data current without manual intervention
    - 🤖 **AI Analytics** — Feeds live metrics into the Claude AI API to generate 
    professional executive summaries, player breakdowns, and head-to-head comparisons
    
    **Tech Stack:**
    `Python` `Pandas` `nba_api` `Streamlit` `Plotly` `Anthropic Claude API` `Schedule`
    
    **Built by:** Andre Tiglao | [GitHub](#)
    """)

df = load_data()
# ── Last Updated Timestamp ────────────────────────────────────────────────────
from datetime import datetime, timedelta
data_mod_time = os.path.getmtime(DATA_PATH)
last_updated = (datetime.fromtimestamp(data_mod_time) + timedelta(hours=1)).strftime("%B %d, %Y at %I:%M %p")
st.caption(f"📅 Data last updated: {last_updated}")

# ── Sidebar Header ────────────────────────────────────────────────────────────
st.sidebar.title("🏀 HoopIQ")
st.sidebar.caption("Built by Andre")
st.sidebar.caption("Powered by Python, Streamlit & Claude AI")
st.sidebar.divider()
st.sidebar.header("Filters")

min_games = st.sidebar.slider("Minimum Games Played", 1, int(df["GP"].max()), 20)
elite_only = st.sidebar.checkbox("Elite Scorers Only")

teams = ["All Teams"] + sorted(df["TEAM"].unique().tolist())
selected_team = st.sidebar.selectbox("Filter by Team", teams)

filtered = df[df["GP"] >= min_games]
if elite_only:
    filtered = filtered[filtered["ELITE_SCORER"] == True]
if selected_team != "All Teams":
    filtered = filtered[filtered["TEAM"] == selected_team]

# ── Stat Leaders ──────────────────────────────────────────────────────────────
st.subheader("🏆 Stat Leaders")

top_scorer = filtered.loc[filtered["PTS_PER_GAME"].idxmax()]
top_assist = filtered.loc[filtered["AST_PER_GAME"].idxmax()]
top_rebounder = filtered.loc[filtered["REB_PER_GAME"].idxmax()]
top_steals = filtered.loc[filtered["STL_PER_GAME"].idxmax()]
top_blocks = filtered.loc[filtered["BLK_PER_GAME"].idxmax()]
top_minutes = filtered.loc[filtered["MIN_PER_GAME"].idxmax()]
elite_count = int(filtered["ELITE_SCORER"].sum())

row1 = st.columns(4)
row1[0].metric("🏀 Points Leader", top_scorer["PLAYER"], delta=f"{top_scorer['PTS_PER_GAME']} PPG")
row1[1].metric("🎯 Assists Leader", top_assist["PLAYER"], delta=f"{top_assist['AST_PER_GAME']} APG")
row1[2].metric("💪 Rebounds Leader", top_rebounder["PLAYER"], delta=f"{top_rebounder['REB_PER_GAME']} RPG")
row1[3].metric("⭐ Elite Scorers", elite_count, )

row2 = st.columns(4)
row2[0].metric("🤺 Steals Leader", top_steals["PLAYER"], delta=f"{top_steals['STL_PER_GAME']} SPG")
row2[1].metric("🛡️ Blocks Leader", top_blocks["PLAYER"], delta=f"{top_blocks['BLK_PER_GAME']} BPG")
row2[2].metric("⏱️ Minutes Leader", top_minutes["PLAYER"], delta=f"{top_minutes['MIN_PER_GAME']} MPG")
row2[3].metric("👥 Players Tracked", len(filtered))

st.caption("⭐ Elite Scorer: players in the top 10% of points per game among all tracked players this season.")

st.divider()

# ── Top Scorers Bar Chart ────────────────────────────────────────────────────
st.subheader("Top 15 Scorers")
top_scorers = filtered.nlargest(15, "PTS_PER_GAME")
fig1 = px.bar(
    top_scorers,
    x="PLAYER",
    y="PTS_PER_GAME",
    color="PTS_PER_GAME",
    color_continuous_scale="Oranges",
    labels={"PTS_PER_GAME": "Points Per Game", "PLAYER": "Player"},
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

# ── Scatter: Points vs Assists ────────────────────────────────────────────────
st.subheader("Points vs Assists")
fig2 = px.scatter(
    filtered,
    x="AST_PER_GAME",
    y="PTS_PER_GAME",
    hover_name="PLAYER",
    color="ELITE_SCORER",
    color_discrete_map={True: "#F7A925", False: "#1D428A"},
    labels={"AST_PER_GAME": "Assists Per Game", "PTS_PER_GAME": "Points Per Game"},
)
st.plotly_chart(fig2, use_container_width=True)

# ── Player Data Explorer ──────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Player Data Explorer")

search = st.text_input("🔍 Search by player name", placeholder="e.g. LeBron, Curry, Jokić...")

display_df = filtered[[
    "PLAYER", "TEAM", "GP", "MIN_PER_GAME",
    "PTS_PER_GAME", "AST_PER_GAME", "REB_PER_GAME",
    "STL_PER_GAME", "BLK_PER_GAME", "ELITE_SCORER"
]].rename(columns={
    "PLAYER": "Player",
    "TEAM": "Team",
    "GP": "Games",
    "MIN_PER_GAME": "MPG",
    "PTS_PER_GAME": "PPG",
    "AST_PER_GAME": "APG",
    "REB_PER_GAME": "RPG",
    "STL_PER_GAME": "SPG",
    "BLK_PER_GAME": "BPG",
    "ELITE_SCORER": "Elite"
}).sort_values("PPG", ascending=False).reset_index(drop=True)

if search:
    display_df = display_df[display_df["Player"].str.contains(search, case=False)]
    if display_df.empty:
        st.warning("No player found.")

st.dataframe(display_df, use_container_width=True, height=400)
st.caption(f"Showing {len(display_df)} players")
# ── AI Executive Summary Section ─────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Analytics")

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ai.summary import load_metrics, generate_summary
import anthropic

tab1, tab2, tab3 = st.tabs(["Season Overview", "Player Summary", "Player Comparison"])

# ── Tab 1: Season Overview ────────────────────────────────────────────────────
with tab1:
    st.caption("Generate an AI-powered overview of the entire current season.")
    if st.button("Generate Season Overview"):
        with st.spinner("Generating..."):
            metrics = load_metrics()
            summary = generate_summary(metrics)
            st.markdown(summary)
            export_path = os.path.join(os.path.dirname(__file__), "..", "data", "executive_summary.txt")
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(summary)
            st.success("Exported to data/executive_summary.txt")

# ── Tab 2: Player Summary ─────────────────────────────────────────────────────
with tab2:
    st.caption("Get an AI-generated breakdown of any player's season performance.")
    player_search = st.text_input("Search player", key="ai_player_search")
    
    if player_search:
        matches = df[df["PLAYER"].str.contains(player_search, case=False)]
        if not matches.empty:
            player_name = st.selectbox("Select player", matches["PLAYER"].tolist())
            
            if st.button("Generate Player Summary"):
                with st.spinner(f"Analyzing {player_name}..."):
                    player = df[df["PLAYER"] == player_name].iloc[0]
                    
                    prompt = f"""
You are a professional NBA analyst. Write a concise 2-paragraph performance
summary for {player['PLAYER']} based on their current season stats.
Be specific, analytical, and professional.

Stats:
- Team: {player['TEAM']}
- Games Played: {player['GP']}
- Minutes Per Game: {player['MIN_PER_GAME']}
- Points Per Game: {player['PTS_PER_GAME']}
- Assists Per Game: {player['AST_PER_GAME']}
- Rebounds Per Game: {player['REB_PER_GAME']}
- Steals Per Game: {player['STL_PER_GAME']}
- Blocks Per Game: {player['BLK_PER_GAME']}
- Elite Scorer: {"Yes" if player['ELITE_SCORER'] else "No"}

Write the summary now:
"""
                    from dotenv import load_dotenv
                    load_dotenv()
                    client = anthropic.Anthropic()
                    message = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown(message.content[0].text)
        else:
            st.warning("No player found.")

# ── Tab 3: Player Comparison ──────────────────────────────────────────────────
with tab3:
    st.caption("Compare two players head to head with AI analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search1 = st.text_input("Search player 1", key="compare_p1")
        if search1:
            matches1 = df[df["PLAYER"].str.contains(search1, case=False)]
            if not matches1.empty:
                player1_name = st.selectbox("Select player 1", matches1["PLAYER"].tolist())
            else:
                st.warning("No player found.")
                player1_name = None
        else:
            player1_name = None

    with col2:
        search2 = st.text_input("Search player 2", key="compare_p2")
        if search2:
            matches2 = df[df["PLAYER"].str.contains(search2, case=False)]
            if not matches2.empty:
                player2_name = st.selectbox("Select player 2", matches2["PLAYER"].tolist())
            else:
                st.warning("No player found.")
                player2_name = None
        else:
            player2_name = None

    if player1_name and player2_name:
        if st.button("Compare Players"):
            with st.spinner(f"Comparing {player1_name} vs {player2_name}..."):
                p1 = df[df["PLAYER"] == player1_name].iloc[0]
                p2 = df[df["PLAYER"] == player2_name].iloc[0]

                prompt = f"""
You are a professional NBA analyst. Write a concise 3-paragraph head to head
comparison between {p1['PLAYER']} and {p2['PLAYER']} based on their current
season stats. Declare a winner at the end with clear reasoning.

{p1['PLAYER']} ({p1['TEAM']}):
- Games Played: {p1['GP']}
- Minutes Per Game: {p1['MIN_PER_GAME']}
- Points Per Game: {p1['PTS_PER_GAME']}
- Assists Per Game: {p1['AST_PER_GAME']}
- Rebounds Per Game: {p1['REB_PER_GAME']}
- Steals Per Game: {p1['STL_PER_GAME']}
- Blocks Per Game: {p1['BLK_PER_GAME']}
- Elite Scorer: {"Yes" if p1['ELITE_SCORER'] else "No"}

{p2['PLAYER']} ({p2['TEAM']}):
- Games Played: {p2['GP']}
- Minutes Per Game: {p2['MIN_PER_GAME']}
- Points Per Game: {p2['PTS_PER_GAME']}
- Assists Per Game: {p2['AST_PER_GAME']}
- Rebounds Per Game: {p2['REB_PER_GAME']}
- Steals Per Game: {p2['STL_PER_GAME']}
- Blocks Per Game: {p2['BLK_PER_GAME']}
- Elite Scorer: {"Yes" if p2['ELITE_SCORER'] else "No"}

Write the comparison now:
"""
                from dotenv import load_dotenv
                load_dotenv()
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(message.content[0].text)