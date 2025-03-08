import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import json

epl = f"https://www.transfermarkt.co.uk/premier-league/formtabelle/wettbewerb/GB1?saison_id=2024&min=1&max="


    
def fetch_league_data(matchweek,league):
    """
    Fetches Premier League data from Transfermarkt for a given matchweek.
    
    Args:
        matchweek (int): The matchweek to fetch data for.

    Returns:
        tuple: A list of club names and a cleaned pandas DataFrame containing the league data.
    """
 

    url = league + str(matchweek)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
   
    liga = soup.find("div", {"class": "data-header__headline-wrapper data-header__headline-wrapper--oswald"}).get_text(strip=True)
    syear = soup.find('option', {'selected': 'selected'})["value"]
    syear_short = soup.find('option', {'selected': 'selected'}).getText()
    syear_long = syear+"/"+ str(int(syear)+1)

    # Extract league table from the page
    table = soup.find_all('table')[1]
    table_rows = table.find_all('tr')
    
    # Extract data from rows
    l = []
    for tr in table_rows[1:]:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    
    # Create a DataFrame with the appropriate columns based on row length
    if len(l[0]) == 11:
        tb = pd.DataFrame(l, columns=["#", "badge", "Club", "MP", "W", "D", "L", "Goals", "+/-", "Pts", "Form"])
    else:
        tb = pd.DataFrame(l, columns=["#", "badge", "Club", "MP", "W", "D", "L", "Goals", "+/-", "Pts"])
    
    # Clean the DataFrame
    tb = tb.drop(columns=['badge'])
    tb = tb.replace(r'\n', ' ', regex=True)
    tb = tb.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Extract the club names into a list
    clubs = tb["Club"].tolist()
 
    # return 
    return clubs, tb, syear, syear_long, syear_short, liga




def add_points(team_name, matchweek, points):
    CSV_FILE = "teams_data.csv"

    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Team"])  # Start with only the "Team" column
        df.to_csv(CSV_FILE, index=False)

    """
    Adds points for a specific matchweek directly into a CSV file.

    Args:
        team_name (str): Name of the team.
        matchweek (str): Matchweek identifier (e.g., 'matchweek_1').
        points (int): Points to add for the given matchweek.
        
    """
    # Load existing data
    df = pd.read_csv(CSV_FILE)

    # Check if matchweek column exists; if not, add it
    if matchweek not in df.columns:
        df[matchweek] = None  # Initialize new matchweek column with NaN

    # Update or insert team data
    if team_name in df["Team"].values:
        df.loc[df["Team"] == team_name, matchweek] = points
    else:
        new_row = {"Team": team_name, matchweek: points}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save back to CSV
    df.to_csv(CSV_FILE, index=False)

def save_points_from_matchweeks(start_matchweek, end_matchweek, league):
    global syear, syear_long, syear_short, liga
    """
    Saves points for all teams across multiple matchweeks into `teams_data`.

    Args:
        start_matchweek (int): The starting matchweek.
        end_matchweek (int): The ending matchweek.
    """
    for matchweek in range(start_matchweek, end_matchweek + 1):
        clubs, tb, syear, syear_long, syear_short, liga = fetch_league_data(matchweek, league)  # Fetch data for the current matchweek
        matchweek_label = f"{matchweek}"  # Generate matchweek label
        for club in clubs:
            # Get points for the current club from the DataFrame
            points = int(tb.query(f'Club == "{club}"')["Pts"].iloc[0])
            add_points(club, matchweek_label, points)  # Add points to the CSV
            
def plot_league():
    # Load the CSV file
    df = pd.read_csv("teams_data.csv")

    # Ensure matchweek columns are integers
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    # Set up the figure
    plt.figure(figsize=(12, 6))

    # Get the list of matchweeks (all columns except 'Team')
    matchweeks = df.columns[1:]
    
    with open('team_colours.json', 'r') as file:
        team_colours = json.load(file)


    # Plot each team
    for index, row in df.iterrows():
        plt.plot(matchweeks, row[1:], marker="o", linestyle="-", label=row["Team"],
                 color=team_colours.get(row["Team"], 'black'))  # Default to black if the team is not in the color dictionary)

    # Add labels and title
    plt.xlabel("Matchweeks")
    plt.ylabel("Points")
    plt.title("Team Performance Across Matchweeks")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Put legend outside plot

    # Save the plot
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot.png")
        
def plot_league_subset(n, option):
    # Load the CSV file
    df = pd.read_csv("teams_data.csv")

    # Ensure matchweek columns are integers
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    # Set up the figure
    plt.figure(figsize=(12, 6))

    # Get the list of matchweeks (all columns except 'Team')
    matchweeks = df.columns[1:]
    
    with open('team_colours.json', 'r') as file:
        team_colours = json.load(file)


    if option == "bot":        
        # Sorts the df based on the final column
        df_sorted = df.sort_values(by=df.columns[-1], ascending=True)
        # Finds the value of the nth smallest value (considering ties)
        threshold_value = df_sorted.iloc[(n - 1), -1]  # Get the value of the 5th smallest row in the last column
        # Select all rows where the final value is less than or equal to the threshold_value
        lowest_rows = df_sorted[df_sorted[df.columns[-1]] <= threshold_value]

        # Plot the selected rows
        for index, row in lowest_rows.iterrows():
            plt.plot(matchweeks, row[1:], marker="o", linestyle="-", label=row["Team"],
                    color=team_colours.get(row["Team"], 'black'))  # Default to black if the team is not in the color dictionary)
        
    if option == "top":
        # Sorts the df based on the final column
        df_sorted = df.sort_values(by=df.columns[-1], ascending=False)
        # Finds the value of the nth smallest value (considering ties)
        threshold_value = df_sorted.iloc[(n - 1), -1]  # Get the value of the 5th smallest row in the last column
        # Select all rows where the final value is less than or equal to the threshold_value
        highest_rows = df_sorted[df_sorted[df.columns[-1]] >= threshold_value]

        # Plot the selected rows
        for index, row in highest_rows.iterrows():
            plt.plot(matchweeks, row[1:], marker="o", linestyle="-", label=row["Team"],
                color=team_colours.get(row["Team"], 'black'))  # Default to black if the team is not in the color dictionary)        

    # Add labels and title
    plt.xlabel("Matchweeks")
    plt.ylabel("Points")
    plt.title("Team Performance Across Matchweeks")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Put legend outside plot

    # Save the plot
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot.png")    
    
    
def plot_teams(teams):
        # Load the CSV file
    df = pd.read_csv("teams_data.csv")

    # Ensure matchweek columns are integers
    df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
    # Set up the figure
    plt.figure(figsize=(12, 6))

    # Get the list of matchweeks (all columns except 'Team')
    matchweeks = df.columns[1:]

    with open('team_colours.json', 'r') as file:
        team_colours = json.load(file)

    filtered_df = df[df.iloc[:, 0].isin(teams)]

    # Plot each team
    for index, row in filtered_df.iterrows():
        plt.plot(matchweeks, row[1:], marker="o", linestyle="-", label=row["Team"],
                color=team_colours.get(row["Team"], 'black'))  # Default to black if the team is not in the color dictionary)


    # Add labels and title
    plt.xlabel("Matchweeks")
    plt.ylabel("Points")
    plt.title("Team Performance Across Matchweeks")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Put legend outside plot

    # Save the plot
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot.png")