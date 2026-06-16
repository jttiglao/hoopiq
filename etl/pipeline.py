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

# ── Main ─────────────────────────────────────────────────────────────────────
def run_pipeline():
    raw = fetch_player_stats()
    clean = clean_player_stats(raw)
    export(clean, "player_stats.csv")
    print(f"Pipeline complete. {len(clean)} players loaded.")
    return clean

if __name__ == "__main__":
    run_pipeline()