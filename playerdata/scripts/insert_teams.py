import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_player_id(cur, ign):
    cur.execute("SELECT id FROM player WHERE ign = %s", (ign,))
    player_id = cur.fetchone()
    return player_id[0] if player_id else None

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="os.environ['DB_NAME']",
    user="os.environ['DB_USER']",
    password="os.environ['DB_PASSWORD']",
    host="os.environ['DB_HOST']",
    port="os.environ['DB_PORT']"
)
cur = conn.cursor()

# Open the data file
with open('teams.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    # Loop through each row in the file
    for row in reader:
        # Get player IDs for each player using their IGN
        player_ids = [
            get_player_id(cur, row['Player 1']),
            get_player_id(cur, row['Player 2']),
            get_player_id(cur, row['Player 3']),
            get_player_id(cur, row['Player 4']),
            get_player_id(cur, row['Player 5']),
        ]

        # Insert the row into the database
        cur.execute("""
            INSERT INTO team (team_name, group_letter, player1_id, player2_id, player3_id, player4_id, player5_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Team Name'],
            row['Group Letter'],
            player_ids[0],
            player_ids[1],
            player_ids[2],
            player_ids[3],
            player_ids[4]
        ))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
