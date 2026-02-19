import pandas as pd

drones = pd.read_csv("data/drone_fleet.csv")
missions = pd.read_csv("data/missions.csv")


def weather_compatible(drone_weather, mission_weather):
    if "Rain" in mission_weather and "IP43" not in drone_weather:
        return False
    return True


def match_drones(project_id):
    mission = missions[missions['project_id'] == project_id].iloc[0]

    compatible = drones[
        (drones['status'] == "Available") &
        (drones['location'] == mission['location'])
    ]

    compatible = compatible[
        compatible['weather_resistance'].apply(
            lambda x: weather_compatible(x, mission['weather_forecast'])
        )
    ]

    return compatible


if __name__ == "__main__":
    print(match_drones("PRJ001"))
