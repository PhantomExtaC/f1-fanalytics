import fastf1
import pandas as pd
import json
import os
from pathlib import Path

# Enable caching so we don't hit the API rate limit again!
CACHE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"

def format_timedelta(td):
    """Helper to format pandas timedelta into M:SS.mmm"""
    if pd.isnull(td): return "N/A"
    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:06.3f}"

def build_weekend_state(year: int):
    print("📡 Booting LapLogic Telemetry Engine...")
    
    schedule = fastf1.get_event_schedule(year)
    now = pd.Timestamp.now().tz_localize(None)
    
    # Look at past events so we are guaranteed to find completed FP2 data
    past_events = schedule[schedule['EventDate'].dt.tz_localize(None) < now]
    
    if past_events.empty:
        print("   -> No past events found for this year.")
        return

    session = None
    # Loop backwards through recent races until we find a valid FP2 (skipping Sprints/Cancellations)
    for _, event in past_events.iloc[::-1].iterrows():
        if event['EventFormat'] == 'testing':
            continue
        
        print(f"   -> Attempting to load FP2 for: {event['EventName']}")
        try:
            session = fastf1.get_session(year, event['EventName'], 'FP2')
            session.load(telemetry=False, weather=True, messages=False)
            _ = session.weather_data
            break # We found a valid session, break the loop!
        except Exception as e:
            print(f"      [!] FP2 unavailable (likely a Sprint weekend). Searching previous race...")
            session = None

    if session is None:
        print("   -> Could not find any valid FP2 data for the season.")
        return

    # 3. Environment: Weather & Track
    weather = session.weather_data.iloc[-1] if not session.weather_data.empty else None
    
    state_data = {
        "track": {
            "circuitName": session.event['EventName'],
            "layoutType": "High Downforce", # Default fallback
            "pitStopDelta": 20.0,
            "drsZones": 2
        },
        "weather": {
            "airTemp": round(weather['AirTemp'], 1) if weather is not None else 25.0,
            "trackTemp": round(weather['TrackTemp'], 1) if weather is not None else 35.0,
            "rainProbability": 0,
            "condition": "Wet" if weather is not None and weather['Rainfall'] > 0 else "Dry"
        },
        "telemetry": {
            "fastestSectors": {},
            "longRunPace": []
        }
    }

    # 4. Performance: Mini-Sectors
    laps = session.laps
    if not laps.empty:
        best_s1 = laps.loc[laps['Sector1Time'].idxmin()]
        best_s2 = laps.loc[laps['Sector2Time'].idxmin()]
        best_s3 = laps.loc[laps['Sector3Time'].idxmin()]
        
        state_data["telemetry"]["fastestSectors"] = {
            "sector1": str(best_s1['Driver']),
            "sector2": str(best_s2['Driver']),
            "sector3": str(best_s3['Driver'])
        }

    # 5. Performance: Long Run Pace (Race Simulation)
    clean_laps = laps.pick_wo_box().pick_track_status('1')
    driver_pace = []
    
    for driver in session.results['Abbreviation']:
        # Fixed the deprecated pick_driver method to pick_drivers
        driver_laps = clean_laps.pick_drivers(driver)
        
        if len(driver_laps) >= 5:
            stints = driver_laps.groupby('Stint')
            longest_stint = stints.size().idxmax()
            stint_laps = driver_laps[driver_laps['Stint'] == longest_stint]
            
            if len(stint_laps) > 3:
                stint_laps = stint_laps.sort_values('LapTime').iloc[1:-1]
            
            avg_time = stint_laps['LapTime'].mean()
            compound = stint_laps['Compound'].iloc[0]
            
            driver_pace.append({
                "driverId": str(driver).lower(),
                "driverName": str(driver),
                "avgLapTime": format_timedelta(avg_time),
                "rawSeconds": avg_time.total_seconds(),
                "tireCompound": str(compound)
            })

    # Sort by fastest average pace
    driver_pace.sort(key=lambda x: x['rawSeconds'])
    for pace in driver_pace:
        del pace['rawSeconds']
        
    # Removed the [:10] slice so it returns all 20 drivers
    state_data["telemetry"]["longRunPace"] = driver_pace

    # 6. Export to JSON
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = EXPORT_DIR / "weekend_state.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ weekend_state.json generated successfully with {len(driver_pace)} drivers!")

if __name__ == "__main__":
    # Dynamically fetch the current year
    current_year = pd.Timestamp.now().year
    build_weekend_state(current_year)