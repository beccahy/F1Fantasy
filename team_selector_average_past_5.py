import random
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from collections import defaultdict

import drivers_meet_cost_cap

conn = sqlite3.connect('f1fantasydb.sqlite')
c = conn.cursor()
c.execute("SELECT DISTINCT gamedayid FROM race_stats ORDER BY gamedayid DESC")
gameday_ids = [int(row[0]) for row in c.fetchall()]

gameday_ids.sort(reverse=True)
gameday_ids = gameday_ids[1:]

last_5_gameday_ids = gameday_ids[1:6]

c.execute("SELECT playerid, gamedayid, total FROM race_stats")
race_data = c.fetchall()

c.execute("SELECT playerid, gamedayid, total FROM race_stats WHERE gamedayid IN (?, ?, ?, ?, ?)", last_5_gameday_ids)
race_data_last_5 = c.fetchall()

conn.close()

# Dictionary to store total scores and race counts for each driver
driver_scores = defaultdict(lambda: [0, 0])  # {playerid: [total_score, race_count]}

# Calculate total scores and race counts
for playerid, gamedayid, total in race_data_last_5:
    driver_scores[playerid][0] += int(total)
    driver_scores[playerid][1] += 1

# Calculate average scores and sort drivers by this score
average_scores = [(playerid, total / count) for playerid, (total, count) in driver_scores.items() if count == 5]
average_scores.sort(key=lambda x: x[1], reverse=True)

drivers_meet_cost_cap.best_team_under_cap(average_scores)

# Select top 5 drivers based on average scores
# top_drivers = [playerid for playerid, avg_score in average_scores[:5]]

# find the total score for all 5 drivers for most recent race week
# player_scores_in_week = defaultdict(int)

# for playerid, gamedayid, total in race_data:
#    if gamedayid == '14' and playerid in top_drivers:
#        player_scores_in_week[playerid] += int(total)

# print(sum(player_scores_in_week.values()))
# print(drivers_meet_cost_cap.is_in_cost_cap(top_drivers))
























