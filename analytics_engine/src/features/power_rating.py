import pandas as pd
from pathlib import Path
import sys

# 1. Safely define paths
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
FEATURE_DATA_DIR = BASE_DIR / "data" / "features"

FEATURE_DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_power_ratings():
    print("📈 Generating Dynamic Power Ratings...")
    
    # 2. Load the Master Data Lake
    master_df = pd.read_csv(RAW_DATA_DIR / "master_historical.csv")
    
    # 3. Enforce Strict Chronology
    # If the data is out of order, the moving averages will pull from the future
    master_df = master_df.sort_values(by=['year', 'round', 'positionOrder']).reset_index(drop=True)
    
    # 4. Constructor Momentum (EMA of Points)
    print("   -> Calculating Constructor Form...")
    # Group by team per race to get total points scored that weekend
    constructor_points = master_df.groupby(['year', 'round', 'constructorRef'])['points'].sum().reset_index()
    
    # Calculate a 10-race exponentially weighted moving average
    # CRITICAL: .shift(1) ensures we only know their momentum GOING INTO the race, preventing data leakage
    constructor_points['team_momentum'] = constructor_points.groupby('constructorRef')['points'].transform(
        lambda x: x.ewm(span=10, min_periods=1).mean().shift(1)
    )
    constructor_points['team_momentum'] = constructor_points['team_momentum'].fillna(0)
    
    # Merge the momentum metric back into the master dataset
    master_df = pd.merge(master_df, constructor_points[['year', 'round', 'constructorRef', 'team_momentum']], 
                         on=['year', 'round', 'constructorRef'], how='left')
    
    # 5. Driver Momentum (EMA of Finishing Position)
    print("   -> Calculating Driver Form...")
    # We use positionOrder instead of points because points are top-10 only. 
    # A driver consistently finishing 11th is fundamentally faster than one finishing 19th.
    master_df['driver_momentum'] = master_df.groupby('driverRef')['positionOrder'].transform(
        lambda x: x.ewm(span=10, min_periods=1).mean().shift(1)
    )
    # Default rookies to the mathematical center of the grid (10.5)
    master_df['driver_momentum'] = master_df['driver_momentum'].fillna(10.5)

    # 6. Driver Racecraft Index (EMA of Positions Gained/Lost)
    print("   -> Calculating Racecraft Index...")
    master_df['positions_gained'] = master_df['grid'] - master_df['positionOrder']
    
    master_df['driver_racecraft_index'] = master_df.groupby('driverRef')['positions_gained'].transform(
        lambda x: x.ewm(span=10, min_periods=1).mean().shift(1)
    )
    master_df['driver_racecraft_index'] = master_df['driver_racecraft_index'].fillna(0)

    # 7. Isolate and Export the Engineered Features
    columns_to_keep = [
        'raceId', 'driverRef', 'team_momentum', 'driver_momentum', 'driver_racecraft_index'
    ]
    power_ratings_df = master_df[columns_to_keep]
    
    output_path = FEATURE_DATA_DIR / "power_ratings.csv"
    power_ratings_df.to_csv(output_path, index=False)
    
    print(f"✅ Dynamic Power Ratings successfully generated!")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    generate_power_ratings()
    input("\nPress Enter to exit...")