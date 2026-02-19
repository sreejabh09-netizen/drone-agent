import pandas as pd

pilots = pd.read_csv("data/pilot_roster.csv")
missions = pd.read_csv("data/missions.csv")


def check_budget(pilot_rate, mission_budget, days):
    cost = pilot_rate * days
    return cost > mission_budget


def detect_conflicts(project_id):
    mission = missions[missions['project_id'] == project_id].iloc[0]

    start = pd.to_datetime(mission['start_date'])
    end = pd.to_datetime(mission['end_date'])
    budget = mission['mission_budget_inr']

    conflicts = []

    for _, pilot in pilots.iterrows():
        if pilot['status'] != "Available":
            conflicts.append(f"{pilot['name']} not available")

        days = (end - start).days + 1

        if check_budget(pilot['daily_rate_inr'], budget, days):
            conflicts.append(f"{pilot['name']} exceeds budget")

    return conflicts


if __name__ == "__main__":
    print(detect_conflicts("PRJ001"))
