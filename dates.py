import json
from datetime import datetime

# Load the JSON file
with open("dates.json", "r") as f:
    matchweeks = json.load(f)

print(type(matchweeks))

# Access data
print(matchweeks[0])  # '2014-08-15'

# # Convert string to datetime
# start_date = datetime.fromisoformat(matchweeks["MW1"]["start"])
# print(start_date)  # 2014-08-15 00:00:00
