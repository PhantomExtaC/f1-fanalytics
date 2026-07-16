import pandas as pd
from pathlib import Path
import os
import sys

# 1. Safely define paths regardless of how the script is executed
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent  # Points to analytics_engine/
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

def bootstrap_historical_data(start_year=2000):
    print("🚀 Starting Historical Data Bootstrap...")
    
    # 2. Load the raw relational tables
    try:
        races = pd.read_csv(RAW_DATA_DIR / "races.csv")
        results = pd.read_csv(RAW_DATA_DIR / "results.csv")
        drivers = pd.read_csv(RAW_DATA_DIR / "drivers.csv")
        constructors = pd.read_csv(RAW_DATA_DIR / "constructors.csv")
        pit_stops = pd.read_csv(RAW_DATA_DIR / "pit_stops.csv")
    except FileNotFoundError as e:
        print(f"❌ ERROR: Missing raw data file. Please ensure CSVs are in {RAW_DATA_DIR}")
        print(e)
        return

    # 3. Filter Races by Year
    races = races[races['year'] >= start_year]
    races = races[['raceId', 'year', 'round', 'circuitId', 'name', 'date']]
    races.rename(columns={'name': 'raceName'}, inplace=True)

    # 4. Merge Results with Races
    master_df = pd.merge(results, races, on='raceId', how='inner')

    # 5. Merge Driver and Constructor Names
    drivers = drivers[['driverId', 'driverRef', 'forename', 'surname']]
    drivers['driverName'] = drivers['forename'] + " " + drivers['surname']
    master_df = pd.merge(master_df, drivers[['driverId', 'driverRef', 'driverName']], on='driverId', how='left')

    constructors = constructors[['constructorId', 'constructorRef', 'name']]
    constructors.rename(columns={'name': 'teamName'}, inplace=True)
    master_df = pd.merge(master_df, constructors, on='constructorId', how='left')

    # 6. Engineer the Tire Degradation Base Metric (Pit Stops)
    print("⚙️ Processing Pit Stop data for Tire Degradation Index...")
    pit_stop_counts = pit_stops.groupby('raceId')['stop'].count().reset_index()
    pit_stop_counts.rename(columns={'stop': 'total_race_pit_stops'}, inplace=True)
    
    master_df = pd.merge(master_df, pit_stop_counts, on='raceId', how='left')
    master_df['total_race_pit_stops'] = master_df['total_race_pit_stops'].fillna(0)

    # 7. Clean and Sort the Final Output
    columns_to_keep = [
        'raceId', 'year', 'round', 'circuitId', 'raceName', 'date',
        'driverRef', 'driverName', 'constructorRef', 'teamName',
        'grid', 'positionOrder', 'points', 'laps', 'statusId', 
        'total_race_pit_stops'
    ]
    master_df = master_df[columns_to_keep]
    master_df = master_df.sort_values(by=['year', 'round', 'positionOrder'])

    # 8. Save the Master Data Lake File
    output_path = RAW_DATA_DIR / "master_historical.csv"
    master_df.to_csv(output_path, index=False)
    
    print(f"✅ Bootstrapping Complete!")
    print(f"📊 Total Records: {len(master_df)}")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    bootstrap_historical_data(start_year=2000)
    # This prevents the window from closing instantly if you double-clicked it
    input("\nPress Enter to exit...")