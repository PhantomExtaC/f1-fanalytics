import pandas as pd
from pathlib import Path
import fastf1
from fastf1.ergast import Ergast
import time
import sys

# 1. Safely define paths
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CACHE_DIR = BASE_DIR / "data" / "cache"

fastf1.Cache.enable_cache(str(CACHE_DIR))

def update_current_season():
    print("🔄 Checking for new race data...")
    
    master_path = RAW_DATA_DIR / "master_historical.csv"
    try:
        master_df = pd.read_csv(master_path)
    except FileNotFoundError:
        print("❌ master_historical.csv not found.")
        sys.exit(1)
        
    # Get the latest state of the database
    current_year = int(pd.Timestamp.now().year)
    
    # Check if we have any data for the current year yet
    if current_year in master_df['year'].values:
        latest_round_in_db = master_df[master_df['year'] == current_year]['round'].max()
    else:
        latest_round_in_db = 0
        
    ergast = Ergast()
    
    try:
        schedule = ergast.get_race_schedule(current_year)
    except Exception as e:
        print(f"❌ Failed to fetch current schedule: {e}")
        sys.exit(1)
        
    # Filter for races that have finished but are NOT in the database yet
    # We add a 1-day buffer to ensure official results are posted
    now = pd.Timestamp.now() - pd.Timedelta(days=1)
    
    missing_races = schedule[
        (schedule['raceDate'] <= now) & 
        (schedule['round'] > latest_round_in_db)
    ]
    
    if missing_races.empty:
        print("✅ Database is fully up to date. No new races to process.")
        return

    new_records = []
    print(f"📥 Found {len(missing_races)} new race(s) to fetch.\n")
    
    for idx, race_info in missing_races.iterrows():
        round_num = race_info['round']
        print(f"Fetching {current_year} Round {round_num}: {race_info['raceName']}...")
        
        try:
            # Add a 2-second delay to be safe with the API limits
            time.sleep(2)
            race = ergast.get_race_results(season=current_year, round=round_num)
            if not race.content or len(race.content) == 0:
                print("   -> Results not officially published yet. Skipping.")
                continue
                
            df = race.content[0].copy()
            
            # Fetch Pit Stops
            time.sleep(1)
            try:
                pit_stops = ergast.get_pit_stops(season=current_year, round=round_num)
                total_pits = len(pit_stops.content[0]) if pit_stops.content else 0
            except:
                total_pits = 0
                
            # Format
            formatted = pd.DataFrame({
                'raceId': (current_year * 100) + round_num,
                'year': current_year,
                'round': round_num,
                'circuitId': race_info['circuitId'],
                'raceName': race_info['raceName'],
                'date': race_info['raceDate'].strftime('%Y-%m-%d'),
                'driverRef': df['driverId'],
                'driverName': df['givenName'] + " " + df['familyName'],
                'constructorRef': df['constructorId'],
                'teamName': df['constructorName'],
                'grid': df['grid'],
                'positionOrder': df['position'],
                'points': df['points'],
                'laps': df['laps'],
                'statusId': df['status'], 
                'total_race_pit_stops': total_pits
            })
            
            new_records.append(formatted)
            print("   -> Success!")
            
        except Exception as e:
            print(f"❌ Error fetching Round {round_num}: {e}")
            
    if new_records:
        new_data_df = pd.concat(new_records, ignore_index=True)
        final_df = pd.concat([master_df, new_data_df], ignore_index=True)
        final_df = final_df.sort_values(by=['year', 'round', 'positionOrder']).reset_index(drop=True)
        final_df.to_csv(master_path, index=False)
        print(f"\n✅ Successfully appended {len(new_data_df)} records to master CSV.")

if __name__ == "__main__":
    update_current_season()