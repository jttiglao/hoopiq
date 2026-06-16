import anthropic
import pandas as pd
import os

# ── Config ───────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "player_stats.csv")

# ── Load Data ────────────────────────────────────────────────────────────────
def load_metrics():
    df = pd.read_csv(DATA_PATH)
    top_scorer = df.loc[df["PTS_PER_GAME"].idxmax()]
    top_assist = df.loc[df["AST_PER_GAME"].idxmax()]
    top_rebounder = df.loc[df["REB_PER_GAME"].idxmax()]
    top_steals = df.loc[df["STL_PER_GAME"].idxmax()]
    top_blocks = df.loc[df["BLK_PER_GAME"].idxmax()]
    top_minutes = df.loc[df["MIN_PER_GAME"].idxmax()]
    elite_count = df["ELITE_SCORER"].sum()

    return {
        "total_players": len(df),
        "elite_scorers": int(elite_count),
        "top_scorer": top_scorer["PLAYER"],
        "top_scorer_ppg": top_scorer["PTS_PER_GAME"],
        "top_assist": top_assist["PLAYER"],
        "top_assist_apg": top_assist["AST_PER_GAME"],
        "top_rebounder": top_rebounder["PLAYER"],
        "top_rebounder_rpg": top_rebounder["REB_PER_GAME"],
        "top_steals": top_steals["PLAYER"],
        "top_steals_spg": top_steals["STL_PER_GAME"],
        "top_blocks": top_blocks["PLAYER"],
        "top_blocks_bpg": top_blocks["BLK_PER_GAME"],
        "top_minutes": top_minutes["PLAYER"],
        "top_minutes_mpg": top_minutes["MIN_PER_GAME"],
    }

# ── Generate Summary ─────────────────────────────────────────────────────────
def generate_summary(metrics: dict) -> str:
    from dotenv import load_dotenv
    load_dotenv()
    client = anthropic.Anthropic()

    prompt = f"""
You are a professional NBA analyst writing an executive summary report.
Based on the following season statistics, write a concise 3-paragraph summary
suitable for a front office executive. Be specific, insightful, and professional.

Season Metrics:
- Total players tracked: {metrics['total_players']}
- Elite scorers (top 10%): {metrics['elite_scorers']}
- Points leader: {metrics['top_scorer']} ({metrics['top_scorer_ppg']} PPG)
- Assists leader: {metrics['top_assist']} ({metrics['top_assist_apg']} APG)
- Rebounds leader: {metrics['top_rebounder']} ({metrics['top_rebounder_rpg']} RPG)
- Steals leader: {metrics['top_steals']} ({metrics['top_steals_spg']} SPG)
- Blocks leader: {metrics['top_blocks']} ({metrics['top_blocks_bpg']} BPG)
- Minutes leader: {metrics['top_minutes']} ({metrics['top_minutes_mpg']} MPG)

Write the executive summary now:
"""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# ── Export Summary ────────────────────────────────────────────────────────────
def export_summary(summary: str):
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "executive_summary.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary exported to {output_path}")

# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading metrics...")
    metrics = load_metrics()
    print("Generating AI summary...")
    summary = generate_summary(metrics)
    print("\n── Executive Summary ──────────────────────────────────────────\n")
    print(summary)
    export_summary(summary)