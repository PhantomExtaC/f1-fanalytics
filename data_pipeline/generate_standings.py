import json
import os
from fastf1.ergast import Ergast

# Initialize the Ergast API client (via FastF1)
ergast = Ergast()

# Define the output path pointing to your React public folder
OUTPUT_DIR = "../public/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_driver_standings(season=2026):
    print(f"Fetching {season} Driver Standings...")
    
    # Fetch the standings
    standings_data = ergast.get_driver_standings(season=season)
    
    # FastF1 returns a Pandas DataFrame inside the 'content' list
    df = standings_data.content[0]
    
    drivers_json = []
    
    # Iterate through the DataFrame rows to build our frontend objects
    for index, row in df.iterrows():
        driver = {
            "id": row['driverId'],
            "position": row['position'],
            "points": float(row['points']),
            "wins": row['wins'],
            "driverName": f"{row['givenName']} {row['familyName']}",
            "driverNumber": row.get('driverNumber', 'N/A'),
            "nationality": row['driverNationality'],
            # Extracting just the first team ID for simplicity
            "currentTeamId": row['constructorIds'][0] if row['constructorIds'] else None,
            # Generate the image path based on your normalized ID strategy
            "imagePath": f"/images/drivers/{row['driverId']}.jpg"
        }
        drivers_json.append(driver)
        
    # Write to JSON
    output_path = os.path.join(OUTPUT_DIR, "driver_standings.json")
    with open(output_path, "w") as f:
        json.dump(drivers_json, f, indent=2)
        
    print(f"✅ Successfully wrote {len(drivers_json)} drivers to {output_path}")

def generate_constructor_standings(season=2026):
    print(f"Fetching {season} Constructor Standings...")
    
    standings_data = ergast.get_constructor_standings(season=season)
    df = standings_data.content[0]
    
    teams_json = []
    
    for index, row in df.iterrows():
        team = {
            "id": row['constructorId'],
            "position": row['position'],
            "points": float(row['points']),
            "wins": row['wins'],
            "teamName": row['constructorName'],
            "nationality": row['constructorNationality'],
            "imagePath": f"/images/teams/{row['constructorId']}.png"
        }
        teams_json.append(team)
        
    output_path = os.path.join(OUTPUT_DIR, "constructor_standings.json")
    with open(output_path, "w") as f:
        json.dump(teams_json, f, indent=2)
        
    print(f"✅ Successfully wrote {len(teams_json)} teams to {output_path}")

if __name__ == "__main__":
    # You can change this to 'current' to always get the active season
    generate_driver_standings(season=2026)
    generate_constructor_standings(season=2026)