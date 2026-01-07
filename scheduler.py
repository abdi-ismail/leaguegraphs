from functions import save_points_from_matchweeks, epl, plot_league
from gotify import send_gotify
import json
from datetime import date

TODAY = date.today().isoformat()


# Load the JSON file
with open("dates.json", "r") as f:
    matchweeks = json.load(f)


for mw in matchweeks:
    if mw["end_date"] == TODAY:
        currentcount = mw["matchweek"]
        try:
            save_points_from_matchweeks(currentcount, currentcount, epl)
            title = "EPL update"
            message = f"Running job for Matchweek {mw['matchweek']}"
            priority = 5
            plot_league("epl", currentcount)
            break

        
        except Exception as e:
            title = "EPL error"
            message = f"Error = {e}"
            priority = 10
                

        finally:
            send_gotify(message=message, title=title, priority=priority )
            print(TODAY, message)
else:
    print(TODAY, "Not today")
