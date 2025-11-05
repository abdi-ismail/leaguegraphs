import schedule
import time
from datetime import datetime

run_dates = ["2025-10-07", "2025-10-10", "2025-10-15"]

def job():
    today = datetime.today().strftime("%Y-%m-%d")
    if today in run_dates:
        print("Running the script!")
    else:
        print("Not today.")

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)


# 1. ZenML (Local Docker Orchestrator)
# 2. n8n (Workflow Automation)
# 3. BYOAI (Agentic Workflow Orchestration)
# 4. Docker Compose
