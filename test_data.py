import pandas as pd

print("Loading data...")

try:
    pilots = pd.read_csv("data/pilot_roster.csv")
    drones = pd.read_csv("data/drone_fleet.csv")
    missions = pd.read_csv("data/missions.csv")

    print("\nPilots Data:")
    print(pilots.head())

    print("\nDrones Data:")
    print(drones.head())

    print("\nMissions Data:")
    print(missions.head())

except Exception as e:
    print("Error:", e)
