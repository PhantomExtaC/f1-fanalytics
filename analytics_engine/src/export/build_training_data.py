import fastf1
import pandas as pd
import os
from pathlib import Path

# Enable caching to save gigabytes of bandwidth and time
CACHE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"

def get_fp2_long_run_pace(session):
    """Extracts the average long run pace for each driver in FP2."""
    session.load(telemetry=False, weather=True, messages=False)
    laps = session.laps.pick_wo_box().pick_track_status('1')
    
    driver_pace = {}
    for driver in session.results['Abbreviation']:
        driver_laps = laps.pick_driver(driver)
        if len(driver_laps) >= 5: # Minimum 5 laps for a representative long run
            stints = driver_laps.groupby('Stint')
            longest_stint = stints.size().idxmax()
            stint_laps = driver_laps[driver_laps['Stint'] == longest_stint]
            
            # Remove outliers
            if len(stint_laps) > 3:
                stint_laps = stint_laps.sort_values('LapTime').iloc[1:-1]
            
            avg_time = stint_laps['LapTime'].mean().total_seconds()
            driver_pace[driver] = avg_time
            
    return driver_pace, session.weather_data['TrackTemp'].mean()

def build_dataset():
    print("🚜 Booting LapLogic Historical Data Scraper...")
    years_to_scrape = [2023, 2024, 2025]
    dataset_rows = []

    for year in years_to_scrape:
        schedule = fastf1.get_event_schedule(year)
        
        for _, event in schedule.iterrows():
            # Skip pre-season testing
            if event['EventFormat'] == 'testing':
                continue
                
            print(f"   -> Processing {year} {event['EventName']}...")
            
            try:
                # 1. Get Friday Data (The Features)
                fp2 = fastf1.get_session(year, event['EventName'], 'FP2')
                driver_pace, track_temp = get_fp2_long_run_pace(fp2)
                
                if not driver_pace:
                    print(f"      [!] No valid FP2 long runs found. Skipping event.")
                    continue
                    
                # Calculate Deficits (The Feature Engineering)
                fastest_pace = min(driver_pace.values())
                deficits = {driver: (pace - fastest_pace) for driver, pace in driver_pace.items()}

                # 2. Get Sunday Data (The Target)
                race = fastf1.get_session(year, event['EventName'], 'R')
                race.load(telemetry=False, weather=False, messages=False)
                
                # Estimate Pit Delta (Average pit lane time for the winner)
                winner_laps = race.laps.pick_driver(race.results.iloc[0]['Abbreviation'])
                pit_laps = winner_laps[winner_laps['PitInTime'].notnull()]
                pit_delta = pit_laps['PitOutTime'].dt.total_seconds().mean() - pit_laps['PitInTime'].dt.total_seconds().mean() if not pit_laps.empty else 20.0

                # 3. Join Features and Target
                for _, result in race.results.iterrows():
                    driver = result['Abbreviation']
                    if driver in deficits:
                        dataset_rows.append({
                            "year": year,
                            "event": event['EventName'],
                            "driver": driver,
                            "track_temp": round(track_temp, 1),
                            "pit_delta": round(pit_delta if pd.notnull(pit_delta) else 20.0, 1),
                            "fp2_deficit": round(deficits[driver], 3),
                            "finishing_position": result['Position'],
                            "won_race": 1 if result['Position'] == 1.0 else 0
                        })
                        
            except Exception as e:
                print(f"      [!] Error processing {event['EventName']}: {e}")
                continue

    # 4. Export the Master Dataset
    df = pd.DataFrame(dataset_rows)
    # Drop rows where drivers DNF'd (Position is NaN) to keep training clean
    df = df.dropna(subset=['finishing_position']) 
    
    export_path = EXPORT_DIR / "f1_historical_training_data.csv"
    df.to_csv(export_path, index=False)
    print(f"\n✅ Dataset complete! Extracted {len(df)} rows. Saved to {export_path}")

if __name__ == "__main__":
    build_dataset()