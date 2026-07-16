import pandas as pd
from pathlib import Path
import fastf1
from fastf1.ergast import Ergast
import time
import random
import sys
import datetime

# 1. Safely define paths
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path(pd.compat.os.getcwd())

BASE_DIR = SCRIPT_DIR.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CACHE_DIR = BASE_DIR / "data" / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

def call_api_with_retry(api_func, *args, **kwargs):
    """Executes an API call with exponential backoff if rate limits are hit."""
    max_retries = 5
    base_delay = 2 
    
    for attempt in range(max_retries):
        try:
            time.sleep(1.0 + random.random()) 
            return api_func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                delay = (base_delay ** attempt) + random.random()
                print(f"\n⚠️ API error/Rate limit hit. Cooling down for {delay:.2f} seconds before retry...")
                time.sleep(delay)
            else:
                raise e

def bridge_gap():
    print("🌉 Bridging the data gap (2024-Present)...")
    
    master_path = RAW_DATA_DIR / "master_historical.csv"
    try:
        master_df = pd.read_csv(master_path)
    except FileNotFoundError:
        print("❌ master_historical.csv not found. Run bootstrap.py first.")
        return
        
    last_year_in_db = int(master_df['year'].max())
    current_year = datetime.datetime.now().year
    
    if last_year_in_db >= current_year:
        print("✅ Master database is already fully up to date.")
        return
        
    start_year = last_year_in_db + 1
    ergast = Ergast()
    new_records = []
    
    print(f"Fetching seasons {start_year} through {current_year}...\n")
    
    for year in range(start_year, current_year + 1):
        print(f"--- Processing Season: {year} ---")
        try:
            schedule = call_api_with_retry(ergast.get_race_schedule, year)
        except Exception as e:
            print(f"Failed to fetch schedule for {year}: {e}")
            continue
            
        # We only want to process races that have already happened
        past_races = schedule[schedule['raceDate'] <= pd.Timestamp.now()].copy()
        
        for idx, race_info in past_races.iterrows():
            round_num = race_info['round']
            print(f"Fetching {year} Round {round_num}: {race_info['raceName']}...", end="\r")
            
            try:
                # 1. Get Race Results
                race = call_api_with_retry(ergast.get_race_results, season=year, round=round_num)
                if not race.content or len(race.content) == 0:
                    continue
                    
                df = race.content[0].copy()
                
                # 2. Get Pit Stops (For our Tire Deg Index)
                try:
                    pit_stops = call_api_with_retry(ergast.get_pit_stops, season=year, round=round_num)
                    total_pits = len(pit_stops.content[0]) if pit_stops.content else 0
                except:
                    # Fallback if pit stop data is unavailable for a new race
                    total_pits = 0
                
                # 3. Format to match Master CSV perfectly
                formatted = pd.DataFrame({
                    # Generate synthetic raceId (e.g. 202401)
                    'raceId': (year * 100) + round_num,
                    'year': year,
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
                    # Ergast status is an ID in historical, but a string here. We just store the string as we don't strictly use it for ML yet.
                    'statusId': df['status'], 
                    'total_race_pit_stops': total_pits
                })
                
                new_records.append(formatted)
                
            except Exception as e:
                print(f"\n❌ Failed to process {year} Round {round_num}: {e}")
                
    if not new_records:
        print("\nNo new completed races found to append.")
        return
        
    print("\n\nConsolidating new data...")
    new_data_df = pd.concat(new_records, ignore_index=True)
    
    # Append to master and save
    final_df = pd.concat([master_df, new_data_df], ignore_index=True)
    final_df = final_df.sort_values(by=['year', 'round', 'positionOrder']).reset_index(drop=True)
    final_df.to_csv(master_path, index=False)
    
    print(f"✅ Bridge Complete! Added {len(new_data_df)} new driver-results to the Data Lake.")
    print(f"📊 The Master Database is now fully updated up to {current_year}.")

if __name__ == "__main__":
    bridge_gap()
    input("\nPress Enter to exit...")