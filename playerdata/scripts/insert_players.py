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
with open('players.csv', 'r', newline='') as f:
    reader = csv.DictReader(f)
    # Loop through each row in the file
    for row in reader:
        # Insert the row into the database
        cur.execute("""
            INSERT INTO player (email_address, first_name, last_name, discord_id, ign, ign2, opgg, peak_rank, primary_role)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Email Address'],
            row['First Name'],
            row['Last Name'],
            row['Discord ID'],
            row['IGN'],
            row['IGN2'] if row['IGN2'] else None,
            row['OPGG'],
            row['Peak Rank'],
            row['Primary Role']  # Add the new "Primary Role" column
        ))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
