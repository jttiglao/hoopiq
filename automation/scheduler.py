import schedule
import time
import sys
import os

# Add root to path so we can import pipeline
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from etl.pipeline import run_pipeline

def run():
    print("Running scheduled pipeline refresh...")
    run_pipeline()
    print("Done.")

# Schedule it to run every day at 6am
schedule.every().day.at("06:00").do(run)

# Also run immediately on startup
run()

print("Scheduler running. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)