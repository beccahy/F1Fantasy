import sqlite3
import numpy as np
import itertools


def is_in_cost_cap(drivers):
    conn = sqlite3.connect('f1fantasydb.sqlite')
    c = conn.cursor()
    c.execute("SELECT current_cost FROM drivers WHERE playerid IN (?, ?, ?, ?, ?)", drivers)
    driver_costs = c.fetchall()
    conn.close()
    driver_costs = [float(i[0]) for i in driver_costs]

    return sum(driver_costs) <= 65


# probs need to optimise this
def best_team_under_cap(average_scores):
    # Step 1: Generate all possible combinations of 5 drivers
    all_combinations = list(itertools.combinations([playerid for playerid, avg_score in average_scores], 5))

    # Step 2: Initialize variables to track the best combination
    best_combination = None
    best_combination_score = -float('inf')  # Start with a very low score

    # Step 3: Iterate through each combination to find the best one under the cost cap
    for combination in all_combinations:
        if is_in_cost_cap(combination):
            # Calculate the total average score for this combination
            total_score = sum(avg_score for playerid, avg_score in average_scores if playerid in combination)

            # Check if this is the best valid combination so far
            if total_score > best_combination_score:
                best_combination = combination
                best_combination_score = total_score

    # Step 4: Output the best combination and its score
    print("Best Combination:", best_combination)
    print("Total Average Score:", best_combination_score)
