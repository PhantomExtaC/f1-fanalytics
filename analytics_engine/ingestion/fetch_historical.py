import pandas as pd
import fastf1
from fastf1.ergast import Ergast
import os
import time
import random
import traceback

from pathlib import Path

print("Initializing Historical Data Fetcher...")

# 1. Get the absolute path of the directory containing this script (ingestion)
SCRIPT_DIR = Path(__file__).resolve().parent

# 2. Go up one level to your main directory (analytics / analytics_engine)
BASE_DIR = SCRIPT_DIR.parent

# 3. Define the data paths securely
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
CACHE_DIR = BASE_DIR / "data" / "cache"

# 4. Create the directories
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# (Optional) Verify the paths in your console
print(f"Raw data will be saved to: {RAW_DATA_DIR}")

print("Starting script...")
print(BASE_DIR)
print(RAW_DATA_DIR)
print(CACHE_DIR)

fastf1.Cache.enable_cache(str(CACHE_DIR))

def call_api_with_retry(api_func, *args, **kwargs):
    """Executes an API call with exponential backoff if rate limits are hit."""
    max_retries = 5
    base_delay = 2  # Start with a 2-second delay on failure
    
    for attempt in range(max_retries):
        try:
            # Respectful short delay before every call to avoid spamming
            time.sleep(1.0 + random.random()) 
            return api_func(*args, **kwargs)
        except Exception as e:
            if "Too Many Requests" in str(e) and attempt < max_retries - 1:
                # Add random jitter to prevent synchronized retry storms
                delay = (base_delay ** attempt) + random.random()
                print(f"\n⚠️ Rate limit hit. Cooling down for {delay:.2f} seconds before retry...")
                time.sleep(delay)
            else:
                # Raise immediately if it's a structural error or ran out of retries
                raise e

def fetch_historical_results(start_year=2019, end_year=2025):
    """Fetches race results using cached sessions and retry safety structures."""
    ergast = Ergast()
    all_results = []
    
    print(f"Starting pipeline: Fetching historical data ({start_year} - {end_year})")
    
    for year in range(start_year, end_year + 1):
        print(f"\n--- Processing Season: {year} ---")
        
        try:
            # Wrap the schedule call with retry logic
            schedule = call_api_with_retry(ergast.get_race_schedule, year)
            total_rounds = len(schedule)
        except Exception as e:
            print(f"Skipping season {year} completely due to critical schedule fetch failure: {e}")
            continue
        
        for round_num in range(1, total_rounds + 1):
            print(f"Fetching Round {round_num}/{total_rounds}...", end="\r")
            try:
                # Wrap the race results call with retry logic
                race = call_api_with_retry(ergast.get_race_results, season=year, round=round_num)
                df = race.content[0]
                
                df['season'] = year
                df['round'] = round_num
                df['circuitId'] = schedule.loc[round_num - 1, 'circuitId']
                
                all_results.append(df)
            except Exception as e:
                print(f"\n❌ Failed permanently for {year} Round {round_num}: {e}")
                
    if not all_results:
        print("❌ Critical: No results collected. Check connectivity.")
        return

    print("\n\nConsolidating data frames...")
    final_df = pd.concat(all_results, ignore_index=True)
    
    output_path = RAW_DATA_DIR / "historical_results.csv"
    final_df.to_csv(output_path, index=False)
    
    print(f"✅ Data Engine successfully generated: {output_path}")

if __name__ == "__main__":
    try:
        fetch_historical_results(2019, 2025)
    except Exception:
        traceback.print_exc()
        input("\nPress Enter to exit...")