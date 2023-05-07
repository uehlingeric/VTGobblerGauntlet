import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Read players.csv and store the data in a dictionary
players = {}
with open('players.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ign = row['IGN']
        ign2 = row['IGN2']
        players[ign] = row
        if ign2:
            players[ign2] = row

# Connect to the GGSpring2023DB
conn = psycopg2.connect(
    dbname="os.environ['DB_NAME']",
    user="os.environ['DB_USER']",
    password="os.environ['DB_PASSWORD']",
    host="os.environ['DB_HOST']",
    port="os.environ['DB_PORT']"
)
cur = conn.cursor()

# Fetch all players who participated in the matches
cur.execute("SELECT DISTINCT player FROM match")
match_players = cur.fetchall()

# Compare the two sets of data and print players who played in a match but are not listed in the players.csv
unlisted_players = []
for player_tuple in match_players:
    player = player_tuple[0]
    if player not in players:
        unlisted_players.append(player)


print("Players who played in a match but are not listed in the players.csv:")
for unlisted_player in unlisted_players:
    print(unlisted_player)

# Close the database connection
cur.close()
conn.close()
