import pandas as pd
from nba_api.stats.endpoints import leagueleaders, teamgamelog
from nba_api.stats.static import teams
import time
import os

# ── Config ──────────────────────────────────────────────────────────────────
SEASON = "2025-26"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# ── Pull player leaders ──────────────────────────────────────────────────────
def fetch_player_stats():
    print("Fetching player stats...")
    time.sleep(1)  # respect rate limit
    leaders = leagueleaders.LeagueLeaders(
        season=SEASON,
        stat_category_abbreviation="PTS"
    )
    df = leaders.get_data_frames()[0]
    return df

# ── Clean + normalize ────────────────────────────────────────────────────────
def clean_player_stats(df):
    print("Cleaning data...")
    df = df.copy()

    # Rename for clarity
    df.columns = [col.upper() for col in df.columns]

    # Drop rows with nulls in key columns
    df.dropna(subset=["PLAYER", "PTS", "AST", "REB"], inplace=True)

    # Add calculated columns
    df["PTS_PER_GAME"] = (df["PTS"] / df["GP"]).round(2)
    df["AST_PER_GAME"] = (df["AST"] / df["GP"]).round(2)
    df["REB_PER_GAME"] = (df["REB"] / df["GP"]).round(2)
    df["STL_PER_GAME"] = (df["STL"] / df["GP"]).round(2)
    df["BLK_PER_GAME"] = (df["BLK"] / df["GP"]).round(2)
    df["MIN_PER_GAME"] = (df["MIN"] / df["GP"]).round(2)

    # Flag elite performers (top 10% in points)
    threshold = df["PTS_PER_GAME"].quantile(0.90)
    df["ELITE_SCORER"] = df["PTS_PER_GAME"] >= threshold

    return df

# ── Export ───────────────────────────────────────────────────────────────────
def export(df, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Exported: {path}")

# ── Pull team stats ──────────────────────────────────────────────────────────
def fetch_team_stats():
    from nba_api.stats.endpoints import leaguestandingsv3, teamestimatedmetrics
    print("Fetching team stats...")
    time.sleep(1)

    # Standings for W/L record
    standings = leaguestandingsv3.LeagueStandingsV3(
        season=SEASON,
        season_type="Regular Season"
    )
    df = standings.get_data_frames()[0]
    return df

def clean_team_stats(df):
    print("Cleaning team stats...")
    df = df.copy()
    df.columns = [col.upper() for col in df.columns]

    # Keep relevant columns
    keep = [
        "TEAMID", "TEAMCITY", "TEAMNAME", "CONFERENCE", "DIVISION",
        "WINS", "LOSSES", "WINPCT", "HOME", "ROAD",
        "POINTSPG", "OPPOINTSPG", "DIFFPOINTSPG",
        "STREAK", "L10"
    ]
    # Only keep columns that exist
    keep = [c for c in keep if c in df.columns]
    df = df[keep]

    df["TEAM"] = df["TEAMCITY"] + " " + df["TEAMNAME"]
    df["WINS"] = pd.to_numeric(df["WINS"], errors="coerce")
    df["LOSSES"] = pd.to_numeric(df["LOSSES"], errors="coerce")
    df["WINPCT"] = pd.to_numeric(df["WINPCT"], errors="coerce").round(3)

    return df

# ── Main ─────────────────────────────────────────────────────────────────────
def run_pipeline():
    # Player stats
    raw = fetch_player_stats()
    clean = clean_player_stats(raw)
    export(clean, "player_stats.csv")
    print(f"Player pipeline complete. {len(clean)} players loaded.")

    # Team stats
    try:
        team_raw = fetch_team_stats()
        team_clean = clean_team_stats(team_raw)
        export(team_clean, "team_stats.csv")
        print(f"Team pipeline complete. {len(team_clean)} teams loaded.")
    except Exception as e:
        print(f"Team stats failed: {e}")

    return clean

if __name__ == "__main__":
    run_pipeline()