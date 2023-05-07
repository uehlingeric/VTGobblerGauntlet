import csv

with open('data.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    next(reader)  # Skip header row

    rows = []
    for row in reader:
        cleaned_row = []
        for value in row:
            if value.isdigit():  # Value is already a number
                cleaned_row.append(int(value))
            elif '.' in value and value.replace('.', '').isdigit():  # Value is a float
                cleaned_row.append(float(value))
            else:  # Value is a string
                cleaned_value = value.replace('"', '').replace(',', '')
                if cleaned_value.isdigit():
                    cleaned_row.append(int(cleaned_value))
                elif '.' in cleaned_value and cleaned_value.replace('.', '').isdigit():
                    cleaned_row.append(float(cleaned_value))
                else:
                    cleaned_row.append(cleaned_value)

        if any(isinstance(value, str) and not value for value in cleaned_row):
            continue  # Skip rows with empty values

        rows.append(cleaned_row)

with open('cleaned_data.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Week', 'Round Robin', 'Match ID', 'Game', 'Result', 'Team', 'Opponent', 'Side', 'Time', 'Player', 'Role', 'Champion', 'Kills', 'Deaths', 'Assists', 'KDA', 'CS', 'CS/min', 'CS diff', 'DMG', 'DMG %', 'DMG/min', 'KP %', 'Gold', 'Gold Share', 'Gold/Min', 'DMG/Gold'])
    writer.writerows(rows)
