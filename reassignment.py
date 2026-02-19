import pandas as pd

pilots = pd.read_csv("data/pilot_roster.csv")


def urgent_reassign(location):
    available = pilots[
        (pilots['status'] == "Available") &
        (pilots['location'] == location)
    ]

    if available.empty:
        return "No pilots available"

    best = available.sort_values("daily_rate_inr").iloc[0]

    return best[['name', 'daily_rate_inr']]


if __name__ == "__main__":
    print(urgent_reassign("Bangalore"))
