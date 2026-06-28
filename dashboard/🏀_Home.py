import streamlit as st

st.set_page_config(page_title="HoopIQ", layout="wide")

st.sidebar.title("🏀 HoopIQ")
st.sidebar.caption("Built by Andre Tiglao")
st.sidebar.caption("Powered by Python, Streamlit & Claude AI")

st.title("🏀 HoopIQ")
st.caption("NBA Performance Intelligence Platform | Season 2025-26 | Data via NBA Stats API")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👤 Player Analytics
    Explore individual player stats, leaders, and AI-powered breakdowns.
    
    - Stat leaders across points, assists, rebounds, steals, blocks
    - Filter by team, games played, and performance tier
    - Player search and data explorer
    - AI player summaries and head-to-head comparisons
    
    → **Navigate to Players in the sidebar**
    """)

with col2:
    st.markdown("""
    ### 🏟️ Team Analytics
    Explore team standings, performance trends, and AI team reports.
    
    - Full league standings with win%, point differential
    - Points per game and differential charts
    - Win% vs PPG scatter analysis
    - AI-generated team performance reports
    
    → **Navigate to Teams in the sidebar**
    """)

st.divider()

with st.expander("ℹ️ About HoopIQ", expanded=False):
    st.markdown("""
    **HoopIQ** is an end-to-end NBA analytics platform built to demonstrate 
    enterprise-grade data engineering and AI-assisted reporting.
    
    **How it works:**
    - 🔄 **ETL Pipeline** — Pulls live player and team stats from the official NBA Stats API, 
    cleans and normalizes the data, and exports master datasets
    - 📊 **Interactive Dashboard** — Filter by team, games played, and performance 
    tier to explore player and team stats dynamically
    - ⏱️ **Automated Refresh** — A scheduler runs the pipeline daily at 6am to keep 
    data current without manual intervention
    - 🤖 **AI Analytics** — Feeds live metrics into the Claude AI API to generate 
    professional executive summaries, player breakdowns, head-to-head comparisons, and team reports
    
    **Tech Stack:**
    `Python` `Pandas` `nba_api` `Streamlit` `Plotly` `Anthropic Claude API` `Schedule`
    
    **Built by:** Andre Tiglao | [GitHub](https://github.com/jttiglao)
    """)

st.markdown("""
### 📊 What's Inside

| Feature | Description |
|---|---|
| Player Stat Leaders | Points, assists, rebounds, steals, blocks, minutes |
| Elite Scorer Flag | Top 10% scorers identified automatically |
| Team Standings | Full league standings with home/away splits |
| Point Differential | Which teams dominate vs struggle |
| AI Season Overview | Claude-generated executive summary |
| AI Player Summary | Per-player breakdown on demand |
| AI Player Comparison | Head-to-head with winner declaration |
| AI Team Report | Team performance analysis on demand |
""")