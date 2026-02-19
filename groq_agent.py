from groq import Groq
import pandas as pd
import gspread

# -------------------------------
# GROQ CLIENT
# -------------------------------
client = Groq(
    api_key="*******************************"
)

# -------------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------------
gc = gspread.service_account(
    r"C:\Users\DELL\Downloads\drone-agent\sheets\credentials.json"
)

sheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1aP6GvofGBIu-mu8a42qgA4jLHUY570hsDUOosAkLJhY/edit?gid=1128986654#gid=1128986654"
).sheet1


# -------------------------------
# LOAD DATA
# -------------------------------
pilots = pd.read_csv("data/pilot_roster.csv")
missions = pd.read_csv("data/missions.csv")
drones = pd.read_csv("data/drone_fleet.csv")

# -------------------------------
# UPDATE PILOT STATUS (WRITE-BACK)
# -------------------------------
def update_pilot_status(name, new_status):

    data = sheet.get_all_records()

    for i, row in enumerate(data):

        if row['name'].lower() == name.lower():
            sheet.update_cell(i + 2, 6, new_status)
            return f"{name} status updated to {new_status}"

    return "Pilot not found."

# -------------------------------
# PILOT MATCHING
# -------------------------------
def match_pilots(project_id):

    mission = missions[
        missions['project_id'] == project_id
    ].iloc[0]

    skill = mission['required_skills']
    location = mission['location']

    eligible = pilots[
        (pilots['skills'].str.contains(skill, case=False)) &
        (pilots['status'] == "Available") &
        (pilots['location'] == location)
    ]

    if eligible.empty:
        return "No eligible pilots found."

    return eligible[
        ['name', 'skills', 'location']
    ].to_string(index=False)

# -------------------------------
# DRONE MATCHING
# -------------------------------
def match_drones(project_id):

    mission = missions[
        missions['project_id'] == project_id
    ].iloc[0]

    location = mission['location']
    weather = mission['weather_forecast']

    available = drones[
        (drones['status'] == "Available") &
        (drones['location'] == location)
    ]

    if "Rain" in weather:
        available = available[
            available['weather_resistance']
            .str.contains("IP43")
        ]

    if available.empty:
        return "No compatible drones available."

    return available[
        ['drone_id', 'model', 'weather_resistance']
    ].to_string(index=False)

# -------------------------------
# CONFLICT DETECTION
# -------------------------------
def detect_conflicts(project_id):

    mission = missions[
        missions['project_id'] == project_id
    ].iloc[0]

    budget = mission['mission_budget_inr']
    days = 3

    alerts = []

    for _, pilot in pilots.iterrows():

        if pilot['status'] != "Available":
            alerts.append(f"{pilot['name']} unavailable")

        cost = pilot['daily_rate_inr'] * days

        if cost > budget:
            alerts.append(f"{pilot['name']} exceeds budget")

    return alerts if alerts else "No conflicts detected."

# -------------------------------
# URGENT REASSIGNMENT
# -------------------------------
def urgent_reassign(location):

    available = pilots[
        (pilots['status'] == "Available") &
        (pilots['location'] == location)
    ]

    if available.empty:
        return "No pilots available for reassignment."

    best = available.sort_values(
        "daily_rate_inr"
    ).iloc[0]

    return f"""
Pilot Name: {best['name']}
Daily Rate: ₹{best['daily_rate_inr']}
Location: {best['location']}
"""

# -------------------------------
# MAIN AGENT FUNCTION
# -------------------------------
def ask_agent(query):

    q = query.lower()


    # 📊 Status Update (Dynamic)

    if "status" in q or "leave" in q or "available" in q:

        # Detect pilot name
        for name in pilots['name']:
            if name.lower() in q:

                # Detect status
                if "leave" in q:
                    return update_pilot_status(name, "On Leave")

                elif "available" in q:
                    return update_pilot_status(name, "Available")

                elif "unavailable" in q:
                    return update_pilot_status(name, "Unavailable")

        return "Pilot name not found in roster."


    # 🧑‍✈️ Pilot Assignment
    if "assign pilot" in q:
        result = match_pilots("PRJ001")
        return f"Eligible pilots:\n{result}"

    # 🚁 Drone Assignment
    if "assign drone" in q:
        result = match_drones("PRJ001")
        return f"Compatible drones:\n{result}"

    # ⚠️ Conflict Detection
    if "conflict" in q:
        result = detect_conflicts("PRJ001")
        return f"Conflict Report:\n{result}"

    # 🔄 Urgent Reassignment
    if "urgent" in q or "reassign" in q:
        result = urgent_reassign("Bangalore")
        return f"Urgent reassignment suggestion:\n{result}"

    # 🤖 Fallback LLM
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a Drone Operations Coordinator AI Agent."
            },
            {
                "role": "user",
                "content": query
            }
        ],
    )

    return completion.choices[0].message.content

# -------------------------------
# TEST RUN
# -------------------------------
if __name__ == "__main__":
    print(ask_agent("Assign pilot for PRJ001"))
