# 🏀 HoopIQ

### NBA Performance Intelligence Platform

An end-to-end data engineering and analytics platform that pulls live NBA
stats, cleans and normalizes the data, visualizes it through an interactive
dashboard, automates daily refreshes, and generates AI-powered executive
reports using the Claude API.

---

## Tech Stack

- **Python** — ETL pipeline, data cleaning, automation
- **nba_api** — Live data source (official NBA Stats API)
- **Pandas** — Data transformation and analysis
- **Streamlit** — Interactive dashboard
- **Plotly** — Dynamic data visualizations
- **Schedule** — Automated daily pipeline refresh
- **Anthropic Claude API** — AI-generated summaries and player analysis

---

## Project Structure

hoopiq/

├── data/ # Processed data outputs

│ ├── player_stats.csv # Master cleaned dataset

│ └── executive_summary.txt

├── etl/

│ └── pipeline.py # Extract, Transform, Load pipeline

├── dashboard/

│ └── app.py # Streamlit dashboard

├── automation/

│ └── scheduler.py # Automated daily refresh

├── ai/

│ └── summary.py # AI executive summary generator

└── README.md

---

## Features

- **ETL Pipeline** — Pulls live player stats from the NBA API, cleans and
  normalizes the data, calculates per game metrics, flags elite scorers,
  and exports a master dataset
- **Interactive Dashboard** — Filter by team, games played, and performance
  tier. View stat leaders across points, assists, rebounds, steals, blocks,
  and minutes
- **Player Data Explorer** — Search any player and view their full stat line
- **Automated Refresh** — Scheduler runs the pipeline daily at 6am keeping
  data current without manual intervention
- **AI Season Overview** — Feeds key metrics into Claude API and generates
  a professional front office executive report
- **AI Player Summary** — Search any player and generate a detailed
  AI-powered performance breakdown
- **AI Player Comparison** — Compare any two players head to head with an
  AI-generated analysis and winner declaration

---

## How to Run

### 1. Clone the repo

```bash
git clone https://github.com/jttiglao/hoopiq.git
cd hoopiq
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install nba_api pandas streamlit plotly anthropic schedule
```

### 4. Set your Anthropic API key

```bash
set ANTHROPIC_API_KEY=your-key-here  # Windows
export ANTHROPIC_API_KEY=your-key-here  # Mac/Linux
```

### 5. Run the ETL pipeline

```bash
python etl/pipeline.py
```

### 6. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

### 7. Generate AI summary standalone

```bash
python ai/summary.py
```

### 8. Run automated scheduler

```bash
python automation/scheduler.py
```

---

## Why I Built This

I wanted to build a project that tied my personal interests with a real-world
data workflow. This project provided me transferable skills that allow me to
create versatile dashboards with AI-assisted analysis, which can be used for
automated reporting. I'd love to be a support engineer and figure out how to
use these skills in the real world.
