import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

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
with open('matches.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    # Loop through each row in the file
    for row in reader:
        # Skip the row if any of the values are blank
        if any(value == '' for value in row.values()):
            continue
        # Convert string values to numbers
        row['Kills'] = int(row['Kills'])
        row['Deaths'] = int(row['Deaths'])
        row['Assists'] = int(row['Assists'])
        row['KDA'] = float(row['KDA'])
        row['CS'] = int(row['CS'])
        row['CS/min'] = float(row['CS/min'])
        row['CS diff'] = int(row['CS diff'])
        row['DMG'] = int(row['DMG'])
        row['DMG %'] = float(row['DMG %'].replace('%', ''))
        row['DMG/min'] = float(row['DMG/min'])
        row['KP %'] = float(row['KP %'].replace('%', ''))
        row['Gold'] = int(row['Gold'])
        row['Gold Share'] = float(row['Gold Share'].replace('%', ''))
        row['Gold/Min'] = float(row['Gold/Min'])
        row['DMG/Gold'] = float(row['DMG/Gold'])

        # Insert the row into the database
        cur.execute("""
                INSERT INTO match (week, round_robin, match_id, game, result, team, opponent, side, time, player, role, champion, kills, deaths, assists, kda, cs, cs_per_min, cs_diff, dmg, dmg_percent, dmg_per_min, kp_percent, gold, gold_share, gold_per_min, dmg_to_gold)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            row['Week'],
            row['Round Robin'],
            row['Match ID'],
            row['Game'],
            row['Result'],
            row['Team'],
            row['Opponent'],
            row['Side'],
            row['Time'],
            row['Player'],
            row['Role'],
            row['Champion'],
            row['Kills'],
            row['Deaths'],
            row['Assists'],
            row['KDA'],
            row['CS'],
            row['CS/min'],
            row['CS diff'],
            row['DMG'],
            row['DMG %'],
            row['DMG/min'],
            row['KP %'],
            row['Gold'],
            row['Gold Share'],
            row['Gold/Min'],
            row['DMG/Gold']
        ))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
