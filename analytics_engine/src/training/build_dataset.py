import pandas as pd
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
FEATURES_DIR = BASE_DIR / "data" / "features"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "model_training_matrix.csv"

def merge_all_features():
    print("🚀 Merging raw race history with engineered feature matrices...")

    # 1. Load the Spine (master_historical.csv)
    master_path = RAW_DIR / "master_historical.csv"
    if not master_path.exists():
        raise FileNotFoundError(f"Missing master file at: {master_path}")
    
    df_master = pd.read_csv(master_path)
    print(f"   -> Loaded {len(df_master)} rows from master_historical.csv")

    # 2. Load the Feature Files
    mastery_path = FEATURES_DIR / "mastery_matrix.csv"
    power_path = FEATURES_DIR / "power_ratings.csv"
    track_path = FEATURES_DIR / "track_profiles.csv"

    df_mastery = pd.read_csv(mastery_path)
    df_power = pd.read_csv(power_path)
    df_track = pd.read_csv(track_path)

    # 3. Perform Left Joins
    # Join driver mastery on [raceId, driverRef]
    df_merged = df_master.merge(
        df_mastery, 
        on=['raceId', 'driverRef'], 
        how='left'
    )

    # Join power ratings on [raceId, driverRef]
    df_merged = df_merged.merge(
        df_power, 
        on=['raceId', 'driverRef'], 
        how='left'
    )

    # Join track profile on [circuitId]
    df_merged = df_merged.merge(
        df_track, 
        on='circuitId', 
        how='left'
    )

    # 4. Clean and Engineer Model Inputs
    # Target variable: 1 if winner, 0 otherwise
    df_merged['won_race'] = (df_merged['positionOrder'] == 1).astype(int)

    # Clean grid: pit-lane starters or unranked (grid <= 0) default to 22
    df_merged['grid'] = pd.to_numeric(df_merged['grid'], errors='coerce').fillna(22)
    df_merged['grid'] = df_merged['grid'].apply(lambda x: 22 if x <= 0 else x)

    # Fill any missing metrics with neutral defaults
    metric_defaults = {
        'driver_overall_avg': 10.5,
        'driver_track_avg': 10.5,
        'driver_street_avg': 10.5,
        'driver_high_deg_avg': 10.5,
        'team_momentum': 0.0,
        'driver_momentum': 10.5,
        'driver_racecraft_index': 0.0,
        'tire_deg_index': 3,
        'is_street': 0,
        'avg_pit_stops': 1.5,
        'total_race_pit_stops': 1.0
    }
    df_merged = df_merged.fillna(value=metric_defaults)

    # 5. Filter for Modern Hybrid Era (2014+) for Relevant Physics & Regulations
    df_train = df_merged[df_merged['year'] >= 2014].copy()

    # 6. Select Final Feature Set
    feature_cols = [
        'raceId', 'year', 'round', 'circuitId',
        'driverRef', 'constructorRef',
        # Core race variables
        'grid', 'total_race_pit_stops',
        # Driver Mastery features
        'driver_overall_avg', 'driver_track_avg', 'driver_street_avg', 'driver_high_deg_avg',
        # Power & Momentum features
        'team_momentum', 'driver_momentum', 'driver_racecraft_index',
        # Track characteristics
        'tire_deg_index', 'is_street', 'avg_pit_stops',
        # Target label
        'won_race'
    ]

    final_matrix = df_train[feature_cols]

    # 7. Export Processed File
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    final_matrix.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Successfully compiled {len(final_matrix)} samples into:")
    print(f"   -> {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_all_features()