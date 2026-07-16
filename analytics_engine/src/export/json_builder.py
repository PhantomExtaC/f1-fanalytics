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
FEATURE_DATA_DIR = BASE_DIR / "data" / "features"
EXPORT_DIR = BASE_DIR.parent / "web_app" / "public" / "data"

# Ensure export directory exists
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def safe_float(val):
    """React breaks if it receives NaN or Infinity. This safely converts them."""
    if pd.isna(val) or math.isnan(val) or math.isinf(val):
        return 0.0
    return round(float(val), 2)

def build_json_exports():
    print("📦 Building JSON Exports for React...")
    
    # 2. Load the Engineered Features
    try:
        power_df = pd.read_csv(FEATURE_DATA_DIR / "power_ratings.csv")
        mastery_df = pd.read_csv(FEATURE_DATA_DIR / "mastery_matrix.csv")
        track_df = pd.read_csv(FEATURE_DATA_DIR / "track_profiles.csv")
    except FileNotFoundError:
        print("❌ ERROR: Feature files not found. Have you run Phase 2?")
        return

    # 3. Compile Current Driver Analytics
    print("   -> Compiling drivers.json & insights.json...")
    
    # We only want the *latest* row for each driver to represent their CURRENT momentum/mastery
    # Since the data is chronological, dropping duplicates and keeping the 'last' occurrence works perfectly
    latest_power = power_df.drop_duplicates(subset=['driverRef'], keep='last')
    latest_mastery = mastery_df.drop_duplicates(subset=['driverRef'], keep='last')
    
    # Merge power and mastery into one snapshot
    driver_snapshot = pd.merge(latest_power, latest_mastery, on=['raceId', 'driverRef'])
    
    # 4. Generate Insights Matrix for the Frontend
    insights_list = []
    
    for _, row in driver_snapshot.iterrows():
        # Determine the driver's strength/weakness dynamically
        # If their street average is lower (better) than high-deg average, they prefer streets
        strength = "Street Circuits" if row['driver_street_avg'] < row['driver_high_deg_avg'] else "High-Degradation Circuits"
        weakness = "High-Degradation Circuits" if strength == "Street Circuits" else "Street Circuits"
        
        insight = {
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
            "profile": {
                "strength": strength,
                "weakness": weakness
            }
        }
        insights_list.append(insight)
        
    # Write insights.json
    insights_path = EXPORT_DIR / "insights.json"
    with open(insights_path, 'w') as f:
        json.dump(insights_list, f, indent=2)
        
    # 5. Compile Track Profiles
    print("   -> Compiling tracksDeg.json...")
    tracks_list = []
    for _, row in track_df.iterrows():
        tracks_list.append({
            "circuitId": row['circuitId'],
            "tireDegradationIndex": int(row['tire_deg_index']),
            "isStreetCircuit": bool(row['is_street']),
            "averagePitStops": safe_float(row['avg_pit_stops'])
        })
        
    # Write tracksDeg.json
    tracks_path = EXPORT_DIR / "tracksDeg.json"
    with open(tracks_path, 'w') as f:
        json.dump(tracks_list, f, indent=2)
        
    print(f"✅ JSON Generation Complete!")
    print(f"💾 Files ready in: {EXPORT_DIR}")

if __name__ == "__main__":
    build_json_exports()
    input("\nPress Enter to exit...")