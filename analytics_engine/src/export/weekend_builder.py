import fastf1
import pandas as pd
import json
from pathlib import Path

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
    
    # 1. Identify the current/next event
    schedule = fastf1.get_event_schedule(year)
    now = pd.Timestamp.now().tz_localize(None)
    upcoming = schedule[schedule['EventDate'].dt.tz_localize(None) >= now]
    
    if upcoming.empty:
        print("   -> Season completed. No live data available.")
        return
        
    next_event = upcoming.iloc[0]
    print(f"   -> Targeting: {next_event['EventName']}")

    # 2. Load the FP2 Session (The Race Simulation session)
    try:
        # We need laps and weather, but we can skip high-frequency car telemetry (speed/throttle) to save load time
        session = fastf1.get_session(year, next_event['EventName'], 'FP2')
        session.load(telemetry=False, weather=True, messages=False)
    except Exception as e:
        print(f"   -> FP2 not yet completed or error loading: {e}")
        return

    # 3. Environment: Weather & Track
    weather = session.weather_data.iloc[-1] if not session.weather_data.empty else None
    
    state_data = {
        "track": {
            "circuitName": session.event['EventName'],
            "layoutType": "Data Pending", # Could be mapped via a static dictionary later
            "pitStopDelta": 20.0, # Average placeholder
            "drsZones": 2
        },
        "weather": {
            "airTemp": round(weather['AirTemp'], 1) if weather is not None else 0,
            "trackTemp": round(weather['TrackTemp'], 1) if weather is not None else 0,
            "rainProbability": 0, # F1 API doesn't provide forecast, only live rainfall
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
    # Filter for laps without pit stops (pick_wo_box) and drop outliers (VSC/Traffic)
    clean_laps = laps.pick_wo_box().pick_track_status('1')
    
    driver_pace = []
    for driver in session.results['Abbreviation']:
        driver_laps = clean_laps.pick_driver(driver)
        
        # A "long run" in FP2 is usually 5+ consecutive laps on the same compound
        if len(driver_laps) >= 5:
            # Group by stint/compound to find the race simulation run
            stints = driver_laps.groupby('Stint')
            longest_stint = stints.size().idxmax()
            stint_laps = driver_laps[driver_laps['Stint'] == longest_stint]
            
            # Remove the absolute fastest and slowest lap of the stint to normalize traffic/errors
            if len(stint_laps) > 3:
                stint_laps = stint_laps.sort_values('LapTime').iloc[1:-1]
            
            avg_time = stint_laps['LapTime'].mean()
            compound = stint_laps['Compound'].iloc[0]
            
            driver_pace.append({
                "driverId": str(driver).lower(),
                "driverName": str(driver),
                "avgLapTime": format_timedelta(avg_time),
                "rawSeconds": avg_time.total_seconds(), # Used for sorting
                "tireCompound": str(compound)
            })

    # Sort by fastest average pace and keep top 10
    driver_pace.sort(key=lambda x: x['rawSeconds'])
    for pace in driver_pace:
        del pace['rawSeconds'] # Clean up before export
        
    state_data["telemetry"]["longRunPace"] = driver_pace[:10]

    # 6. Export to JSON
    export_path = EXPORT_DIR / "weekend_state.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, indent=2, ensure_ascii=False)
        
    print("   -> weekend_state.json generated successfully!")