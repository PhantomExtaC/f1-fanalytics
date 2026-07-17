import pandas as pd
import json
from pathlib import Path
import math

# 1. Setup Paths
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FEATURE_DATA_DIR = BASE_DIR / "data" / "features"
EXPORT_DIR = BASE_DIR.parent / "web_app" / "public" / "data"

# Ensure export directory exists
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def safe_float(val):
    """Safely converts NaN or Infinity values to prevent breaking React JSON parsers."""
    if pd.isna(val) or math.isnan(val) or math.isinf(val):
        return 0.0
    return round(float(val), 2)

def build_json_exports():
    print("📦 Building Advanced JSON Exports for React Charts...")
    
    # 2. Load the Master Lake and Engineered Features
    try:
        master_df = pd.read_csv(RAW_DATA_DIR / "master_historical.csv")
        power_df = pd.read_csv(FEATURE_DATA_DIR / "power_ratings.csv")
        mastery_df = pd.read_csv(FEATURE_DATA_DIR / "mastery_matrix.csv")
        track_df = pd.read_csv(FEATURE_DATA_DIR / "track_profiles.csv")
    except FileNotFoundError as e:
        print(f"❌ ERROR: Required data file missing: {e}")
        return

    # Ensure everything is in chronological order for time-series extraction
    master_df = master_df.sort_values(by=['year', 'round', 'positionOrder']).reset_index(drop=True)
    
    # Attach driver reference to power features for merging
    power_full = pd.merge(master_df[['raceId', 'year', 'round', 'driverRef']], power_df, on=['raceId', 'driverRef'])

    # =========================================================================
    # STEP 1: Current Season Points Progression (pointsProgression.json)
    # =========================================================================
    print("   -> Engineering current season points progression chart data...")
    current_year = int(master_df['year'].max())
    season_data = master_df[master_df['year'] == current_year].copy()
    
    # Calculate running cumulative points total for each driver
    season_data = season_data.sort_values(by=['driverRef', 'round'])
    season_data['cum_points'] = season_data.groupby('driverRef')['points'].cumsum()
    
    # Pivot the data into a Round-Centric format optimized for React Recharts
    # Format: [ { "round": 1, "hamilton": 25, "verstappen": 18 }, ... ]
    max_round = int(season_data['round'].max())
    progression_list = []
    
    for r in range(1, max_round + 1):
        round_slice = season_data[season_data['round'] == r]
        round_entry = {"round": r}
        
        # Populate each active driver's points total at this exact round boundary
        for _, row in round_slice.iterrows():
            round_entry[row['driverRef']] = int(row['cum_points'])
            
        # Forward-fill drivers who missed a round so their line chart doesn't break
        if progression_list:
            prev_entry = progression_list[-1]
            for driver in prev_entry:
                if driver != "round" and driver not in round_entry:
                    round_entry[driver] = prev_entry[driver]
                    
        progression_list.append(round_entry)
        
    with open(EXPORT_DIR / "pointsProgression.json", 'w') as f:
        json.dump(progression_list, f, indent=2)

    # =========================================================================
    # STEP 2: Driver Dynamic Form Trends (driverTrends.json)
    # =========================================================================
    print("   -> Engineering historical form trendlines for sparkline charts...")
    trends_dict = {}
    
    # Extract the last 6 races of form history for every driver to power sparklines
    unique_drivers = power_full['driverRef'].unique()
    for driver in unique_drivers:
        driver_history = power_full[power_full['driverRef'] == driver].tail(6)
        
        trends_dict[driver] = {
            "momentumHistory": [safe_float(x) for x in driver_history['driver_momentum'].tolist()],
            "racecraftHistory": [safe_float(x) for x in driver_history['driver_racecraft_index'].tolist()]
        }
        
    with open(EXPORT_DIR / "driverTrends.json", 'w') as f:
        json.dump(trends_dict, f, indent=2)

    # =========================================================================
    # STEP 3: Structural Snapshots (insights.json & tracksDeg.json)
    # =========================================================================
    print("   -> Updating structural profiles (insights.json & tracksDeg.json)...")
    latest_power = power_df.drop_duplicates(subset=['driverRef'], keep='last')
    latest_mastery = mastery_df.drop_duplicates(subset=['driverRef'], keep='last')
    driver_snapshot = pd.merge(latest_power, latest_mastery, on=['raceId', 'driverRef'])
    
    insights_list = []
    for _, row in driver_snapshot.iterrows():
        strength = "Street Circuits" if row['driver_street_avg'] < row['driver_high_deg_avg'] else "High-Degradation Circuits"
        weakness = "High-Degradation Circuits" if strength == "Street Circuits" else "Street Circuits"
        
        insights_list.append({
            "driverId": row['driverRef'],
            "powerRating": {
                "momentumIndex": safe_float(row['driver_momentum']),
                "racecraftIndex": safe_float(row['driver_racecraft_index'])
            },
            "mastery": {
                "overallAverage": safe_float(row['driver_overall_avg']),
                "streetAverage": safe_float(row['driver_street_avg']),
                "highDegAverage": safe_float(row['driver_high_deg_avg'])
            },
            "profile": { "strength": strength, "weakness": weakness }
        })
        
    with open(EXPORT_DIR / "insights.json", 'w') as f:
        json.dump(insights_list, f, indent=2)
        
    tracks_list = []
    for _, row in track_df.iterrows():
        tracks_list.append({
            "circuitId": row['circuitId'],
            "tireDegradationIndex": int(row['tire_deg_index']),
            "isStreetCircuit": bool(row['is_street']),
            "averagePitStops": safe_float(row['avg_pit_stops'])
        })
        
    with open(EXPORT_DIR / "tracksDeg.json", 'w') as f:
        json.dump(tracks_list, f, indent=2)
        
    print(f"✅ Data Factory Export Complete! React data lake refreshed in: {EXPORT_DIR}")

if __name__ == "__main__":
    build_json_exports()