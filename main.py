from functions import *

file_path = "teams_data.csv"

if os.path.exists(file_path):
    df = pd.read_csv("teams_data.csv")
    last_count = int(df.columns[-1])
    count = last_count + 1
else:
    count = 1

def nextweek():
    global count
    save_points_from_matchweeks(count, count, epl)
    count += 1
    
nextweek()
plot_league()