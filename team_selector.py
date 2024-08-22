import random
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from collections import defaultdict

import drivers_meet_cost_cap

conn = sqlite3.connect('f1fantasydb.sqlite')
c = conn.cursor()
get_drivers_sql = """
            SELECT playerid FROM drivers;
            """
c.execute(get_drivers_sql)
drivers = [row[0] for row in c.fetchall()]


random_selections = [random.sample(drivers, 5) for _ in range(1000)]

c.execute("SELECT playerid, gamedayid, total FROM race_stats")
race_data = c.fetchall()

c.execute("SELECT DISTINCT gamedayid FROM race_stats")
gameday_ids = [row[0] for row in c.fetchall()]


# calculate total scores for selection
# Create a dictionary to store player scores
driver_scores = defaultdict(lambda: defaultdict(int))

conn.close()

total_scores = []

# Calculate total scores for each random selection
for selection in random_selections:
    if drivers_meet_cost_cap.is_in_cost_cap(selection):
        weekly_totals = [(gamedayid, 0) for gamedayid in gameday_ids]  # Initialize with zeros
        for playerid in selection:
            for row in race_data:
                if row[0] == playerid:
                    gamedayid = row[1]
                    total = int(row[2])  # Convert total to integer
                    # Add total to corresponding gamedayid in weekly_totals
                    for i, (gid, score) in enumerate(weekly_totals):
                        if gid == gamedayid:
                            weekly_totals[i] = (gid, score + total)
                            break

        total_scores.append(weekly_totals)


# Example for plotting the total score for gameday 1
gameday_id = '14'
gameday_scores = [score for totals in total_scores for gid, score in totals if gid == gameday_id]

# Plotting
plt.hist(gameday_scores, bins=50, alpha=0.75, color='blue')
plt.title(f'Distribution of Total Scores for Randomly Selected 5 Drivers (Gameday {gameday_id})')
plt.xlabel('Total Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()






















