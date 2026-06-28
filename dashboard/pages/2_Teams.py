import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import anthropic
from dotenv import load_dotenv

load_dotenv()

TEAM_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "team_stats.csv")

st.set_page_config(
    page_title="HoopIQ",
    page_icon="🏀",
    layout="wide"
)

st.sidebar.title("🏀 HoopIQ")
st.sidebar.caption("Built by Andre Tiglao")
st.sidebar.caption("Powered by Python, Streamlit & Claude AI")
st.sidebar.divider()
st.sidebar.header("Filters")

@st.cache_data(ttl=0)
def load_team_data():
    if not os.path.exists(TEAM_DATA_PATH):
        return None
    return pd.read_csv(TEAM_DATA_PATH)

team_df = load_team_data()

st.title("🏟️ Team Analytics")
st.caption("Season 2025-26 | Data via NBA Stats API")

if team_df is None:
    st.error("Team data not found. Run the ETL pipeline first.")
    st.stop()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
conf_options = ["All"] + sorted(team_df["CONFERENCE"].dropna().unique().tolist())
selected_conf = st.sidebar.selectbox("Filter by Conference", conf_options)

team_filtered = team_df.copy()
if selected_conf != "All":
    team_filtered = team_filtered[team_filtered["CONFERENCE"] == selected_conf]

team_filtered = team_filtered.sort_values("WINS", ascending=False)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.subheader("📊 League Overview")

best_team = team_filtered.iloc[0]
worst_team = team_filtered.iloc[-1]
avg_pts = round(team_filtered["POINTSPG"].mean(), 1)
avg_diff = round(team_filtered["DIFFPOINTSPG"].mean(), 1)

t1, t2, t3, t4 = st.columns(4)
t1.metric("🏆 Best Record", best_team["TEAM"], delta=f"{int(best_team['WINS'])}W - {int(best_team['LOSSES'])}L")
t2.metric("📉 Worst Record", worst_team["TEAM"], delta=f"{int(worst_team['WINS'])}W - {int(worst_team['LOSSES'])}L")
t3.metric("🏀 Avg PPG", avg_pts)
t4.metric("📊 Avg Point Diff", avg_diff)

st.divider()

# ── Standings Table ───────────────────────────────────────────────────────────
st.subheader("Standings")

standings_display = team_filtered[[
    "TEAM", "CONFERENCE", "DIVISION", "WINS", "LOSSES",
    "WINPCT", "POINTSPG", "DIFFPOINTSPG", "HOME", "ROAD", "L10"
]].rename(columns={
    "TEAM": "Team", "CONFERENCE": "Conf", "DIVISION": "Division",
    "WINS": "W", "LOSSES": "L", "WINPCT": "Win%",
    "POINTSPG": "PPG", "DIFFPOINTSPG": "+/-",
    "HOME": "Home", "ROAD": "Away", "L10": "Last 10",
}).reset_index(drop=True)

st.dataframe(standings_display, use_container_width=True, height=400)

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
st.subheader("Points Per Game by Team")
fig_pts = px.bar(
    team_filtered.sort_values("POINTSPG", ascending=False),
    x="TEAM",
    y="POINTSPG",
    color="POINTSPG",
    color_continuous_scale="Blues",
    labels={"POINTSPG": "Points Per Game", "TEAM": "Team"},
)
fig_pts.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_pts, use_container_width=True)

st.subheader("Point Differential by Team")
fig_diff = px.bar(
    team_filtered.sort_values("DIFFPOINTSPG", ascending=False),
    x="TEAM",
    y="DIFFPOINTSPG",
    color="DIFFPOINTSPG",
    color_continuous_scale="RdYlGn",
    labels={"DIFFPOINTSPG": "Point Differential", "TEAM": "Team"},
)
fig_diff.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_diff, use_container_width=True)

st.subheader("Win% vs Points Per Game")
fig_scatter = px.scatter(
    team_filtered,
    x="POINTSPG",
    y="WINPCT",
    hover_name="TEAM",
    color="CONFERENCE",
    size="WINS",
    labels={"POINTSPG": "Points Per Game", "WINPCT": "Win%", "CONFERENCE": "Conference"},
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── AI Team Report ────────────────────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Team Report")

selected_team_ai = st.selectbox("Select a team", team_filtered["TEAM"].tolist())

if st.button("Generate Team Report"):
    with st.spinner(f"Analyzing {selected_team_ai}..."):
        t = team_filtered[team_filtered["TEAM"] == selected_team_ai].iloc[0]
        prompt = f"""You are a professional NBA analyst. Write a concise 2-paragraph analysis of the {t['TEAM']} based on their current season stats. Be specific and insightful.

Stats:
- Record: {int(t['WINS'])}W - {int(t['LOSSES'])}L ({t['WINPCT']} win%)
- Conference: {t['CONFERENCE']}
- Points Per Game: {t['POINTSPG']}
- Point Differential: {t['DIFFPOINTSPG']}
- Home Record: {t['HOME']}
- Away Record: {t['ROAD']}
- Last 10 Games: {t['L10']}

Write the analysis now:"""

        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown(message.content[0].text)