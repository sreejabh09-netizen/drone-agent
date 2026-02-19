import pandas as pd

# Load data
pilots = pd.read_csv("data/pilot_roster.csv")
missions = pd.read_csv("data/missions.csv")


def match_pilots_to_mission(project_id):
    mission = missions[missions['project_id'] == project_id].iloc[0]

    required_skill = mission['required_skills']
    required_cert = mission['required_certs']
    location = mission['location']

    eligible = pilots[
        (pilots['skills'].str.contains(required_skill, case=False)) &
        (pilots['certifications'].str.contains(required_cert.split(',')[0], case=False)) &
        (pilots['status'] == "Available") &
        (pilots['location'] == location)
    ]

    return eligible


# Test
if __name__ == "__main__":
    result = match_pilots_to_mission("PRJ001")
    print(result)
