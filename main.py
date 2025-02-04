#!/usr/bin/env python3
from functions import *

file_path = "count.txt"

# Check if file exists and load it, otherwise initialize count
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        count = int(f.read())
else:
    count = 1  # Default value if file does not exist
    with open(file_path, "w") as f:
        f.write(str(count))

def nextweek():
    global count
    save_points_from_matchweeks(count, count, epl)
    count += 1
    with open(file_path, "w") as f:
        f.write(str(count))

while count < 25: 
     nextweek()
plot_league()


