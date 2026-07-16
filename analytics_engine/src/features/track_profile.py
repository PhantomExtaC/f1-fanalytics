import pandas as pd
from pathlib import Path
import numpy as np

# 1. Setup Paths
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FEATURE_DATA_DIR = BASE_DIR / "data" / "features"

# Ensure the features directory exists
FEATURE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 2. Hardcoded domain knowledge for Street Circuits
# While pit stops are mathematical, circuit layout types are geographical facts.
STREET_CIRCUITS = [
    'monaco', 'marina_bay', 'albert_park', 'baku', 'jeddah', 
    'miami', 'vegas', 'valencia', 'montreal', 'sochi', 'madrid'
]

def generate_track_profiles():
    print("🌍 Generating Track Fingerprints...")
    
    # 3. Load the Master Data Lake
    master_df = pd.read_csv(RAW_DATA_DIR / "master_historical.csv")
    
    # 4. Isolate Unique Races to calculate Pit Stop averages
    # We drop duplicate rows so we only look at 1 row per race
    races_df = master_df[['raceId', 'circuitId', 'total_race_pit_stops']].drop_duplicates()
    
    # Filter out anomaly races (0 pit stops usually means a weather red flag like Spa 2021, 
    # or old data missing from Ergast)
    valid_races = races_df[races_df['total_race_pit_stops'] > 0]
    
    # 5. Calculate Average Pit Stops per Circuit
    track_stats = valid_races.groupby('circuitId')['total_race_pit_stops'].mean().reset_index()
    track_stats.rename(columns={'total_race_pit_stops': 'avg_pit_stops'}, inplace=True)
    
    # 6. Engineer the Tire Degradation Index (1 to 5 Scale)
    # We use Pandas 'qcut' (Quantile Cut) to automatically divide the circuits 
    # into 5 even buckets based on their pit stop averages.
    # 1 = Very Low Deg (e.g. Monza), 5 = Very High Deg (e.g. Suzuka/Bahrain)
    track_stats['tire_deg_index'] = pd.qcut(
        track_stats['avg_pit_stops'], 
        q=5, 
        labels=[1, 2, 3, 4, 5]
    ).astype(int)
    
    # 7. Map Street Circuits (1 for Street, 0 for Permanent)
    track_stats['is_street'] = track_stats['circuitId'].apply(
        lambda x: 1 if x in STREET_CIRCUITS else 0
    )
    
    # 8. Save the Engineered Features
    output_path = FEATURE_DATA_DIR / "track_profiles.csv"
    track_stats.to_csv(output_path, index=False)
    
    print(f"✅ Track Profiles successfully generated!")
    print(f"💾 Saved to: {output_path}")
    print("\n--- Preview of Track Fingerprints ---")
    
    # Show a preview of a few famous tracks to verify accuracy
    preview = track_stats[track_stats['circuitId'].isin(['monaco', 'bahrain', 'monza', 'silverstone'])]
    print(preview.to_string(index=False))

if __name__ == "__main__":
    generate_track_profiles()
    input("\nPress Enter to exit...")