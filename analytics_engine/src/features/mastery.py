import pandas as pd
from pathlib import Path

try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FEATURE_DATA_DIR = BASE_DIR / "data" / "features"

def generate_mastery_matrix():
    print("🧠 Engineering Driver-Track Mastery Matrix...")
    
    # 1. Load Data
    master_df = pd.read_csv(RAW_DATA_DIR / "master_historical.csv")
    track_profiles = pd.read_csv(FEATURE_DATA_DIR / "track_profiles.csv")
    
    # Merge track profiles into master to get 'is_street' and 'tire_deg_index' per race row
    df = pd.merge(master_df, track_profiles[['circuitId', 'is_street', 'tire_deg_index']], on='circuitId', how='left')
    
    # Enforce strict chronological order
    df = df.sort_values(by=['year', 'round', 'positionOrder']).reset_index(drop=True)
    
    # 2. Career Core Baseline (Overall Average)
    df['driver_overall_avg'] = df.groupby('driverRef')['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 3. Track-Specific Baseline
    df['driver_track_avg'] = df.groupby(['driverRef', 'circuitId'])['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 4. Street Circuit Mastery Baseline
    df['driver_street_avg'] = df.groupby(['driverRef', 'is_street'])['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 5. High-Degradation Mastery Baseline (Tire Deg Index >= 4)
    df['is_high_deg'] = df['tire_deg_index'].apply(lambda x: 1 if x >= 4 else 0)
    df['driver_high_deg_avg'] = df.groupby(['driverRef', 'is_high_deg'])['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 6. Sequential Fallback Logic (Hierarchical Imputation)
    # If a driver has never raced at this specific track before:
    # Look at their track-style average first, then overall average, then fallback to grid midpoint
    df['driver_track_avg'] = df['driver_track_avg'].fillna(df['driver_street_avg'])
    df['driver_track_avg'] = df['driver_track_avg'].fillna(df['driver_overall_avg'])
    
    # Final rookie protections if everything is NaN
    df['driver_track_avg'] = df['driver_track_avg'].fillna(10.5)
    df['driver_overall_avg'] = df['driver_overall_avg'].fillna(10.5)
    df['driver_street_avg'] = df['driver_street_avg'].fillna(10.5)
    df['driver_high_deg_avg'] = df['driver_high_deg_avg'].fillna(10.5)
    
    # 7. Isolate and Export Matrix Features
    columns_to_export = [
        'raceId', 'driverRef', 'driver_overall_avg', 'driver_track_avg', 
        'driver_street_avg', 'driver_high_deg_avg'
    ]
    mastery_df = df[columns_to_export]
    
    output_path = FEATURE_DATA_DIR / "mastery_matrix.csv"
    mastery_df.to_csv(output_path, index=False)
    
    print(f"✅ Driver-Track Mastery Matrix successfully generated!")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    generate_mastery_matrix()
    input("\nPress Enter to exit...")