import fastf1
import pandas as pd
import json
import os
from pathlib import Path

# Enable caching so we don't hit API rate limits
CACHE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "f1_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"


def format_timedelta(td):
    """Helper to format pandas timedelta into M:SS.mmm"""
    if pd.isnull(td):
        return "N/A"
    total_seconds = td.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:06.3f}"


def build_weekend_state(year: int):
    print("📡 Booting LapLogic Telemetry Engine...")

    schedule = fastf1.get_event_schedule(year)
    now = pd.Timestamp.now().tz_localize(None)

    # 1. Identify the upcoming target event from the schedule
    upcoming_events = schedule[schedule['EventDate'].dt.tz_localize(None) >= now]
    
    if upcoming_events.empty:
        # Fallback to the season finale if the season is finished
        target_event = schedule.iloc[-1]
        print(f"   -> Season completed. Defaulting to finale: {target_event['EventName']}")
    else:
        target_event = upcoming_events.iloc[0]
        print(f"   -> Target Upcoming Race: {target_event['EventName']}")

    # 2. Attempt to load live FP2 data for the target event; fallback to recent valid session if pending
    session = None
    
    try:
        print(f"   -> Checking for live FP2 session: {target_event['EventName']}...")
        live_session = fastf1.get_session(year, target_event['EventName'], 'FP2')
        live_session.load(telemetry=False, weather=True, messages=False)
        _ = live_session.weather_data
        session = live_session
        print(f"   -> ✅ Successfully loaded live FP2 for {target_event['EventName']}")
    except Exception:
        print(f"   -> Live FP2 not yet available for {target_event['EventName']}. Loading latest completed telemetry...")
        past_events = schedule[schedule['EventDate'].dt.tz_localize(None) < now]
        
        for _, event in past_events.iloc[::-1].iterrows():
            if event['EventFormat'] == 'testing':
                continue
            try:
                hist_session = fastf1.get_session(year, event['EventName'], 'FP2')
                hist_session.load(telemetry=False, weather=True, messages=False)
                _ = hist_session.weather_data
                session = hist_session
                print(f"   -> Using baseline telemetry from: {event['EventName']}")
                break
            except Exception:
                continue

    if session is None:
        print("❌ Could not load any valid session data.")
        return

    # 3. Environment: Weather & Track Profile (Anchored to Target Event)
    weather = session.weather_data.iloc[-1] if not session.weather_data.empty else None

    state_data = {
        "track": {
            "circuitName": str(target_event['EventName']),
            "layoutType": "High Downforce",
            "pitStopDelta": 20.0,
            "drsZones": 2
        },
        "weather": {
            "airTemp": round(float(weather['AirTemp']), 1) if weather is not None and 'AirTemp' in weather else 25.0,
            "trackTemp": round(float(weather['TrackTemp']), 1) if weather is not None and 'TrackTemp' in weather else 35.0,
            "rainProbability": 0,
            "condition": "Wet" if (weather is not None and weather.get('Rainfall', 0) > 0) else "Dry"
        },
        "telemetry": {
            "fastestSectors": {},
            "longRunPace": []
        }
    }

    # 4. Mini-Sectors
    laps = session.laps
    if not laps.empty:
        s1_laps = laps.dropna(subset=['Sector1Time'])
        s2_laps = laps.dropna(subset=['Sector2Time'])
        s3_laps = laps.dropna(subset=['Sector3Time'])

        state_data["telemetry"]["fastestSectors"] = {
            "sector1": str(s1_laps.loc[s1_laps['Sector1Time'].idxmin()]['Driver']) if not s1_laps.empty else "N/A",
            "sector2": str(s2_laps.loc[s2_laps['Sector2Time'].idxmin()]['Driver']) if not s2_laps.empty else "N/A",
            "sector3": str(s3_laps.loc[s3_laps['Sector3Time'].idxmin()]['Driver']) if not s3_laps.empty else "N/A"
        }

    # 5. Long Run Pace (Race Simulation)
    clean_laps = laps.pick_wo_box().pick_track_status('1')
    driver_pace = []

    for driver in session.results['Abbreviation']:
        driver_laps = clean_laps.pick_drivers(driver)

        if len(driver_laps) >= 4:
            stints = driver_laps.groupby('Stint')
            longest_stint = stints.size().idxmax()
            stint_laps = driver_laps[driver_laps['Stint'] == longest_stint]

            if len(stint_laps) > 2:
                stint_laps = stint_laps.sort_values('LapTime').iloc[1:-1]

            avg_time = stint_laps['LapTime'].mean()
            compound = stint_laps['Compound'].iloc[0] if ('Compound' in stint_laps and not stint_laps['Compound'].empty) else "MEDIUM"

            driver_pace.append({
                "driverId": str(driver).lower(),
                "driverName": str(driver),
                "avgLapTime": format_timedelta(avg_time),
                "rawSeconds": avg_time.total_seconds(),
                "tireCompound": str(compound)
            })

    # Sort descending by pace
    driver_pace.sort(key=lambda x: x['rawSeconds'])
    for pace in driver_pace:
        del pace['rawSeconds']

    state_data["telemetry"]["longRunPace"] = driver_pace

    # 6. Export to JSON
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = EXPORT_DIR / "weekend_state.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, indent=2, ensure_ascii=False)

    print(f"✅ weekend_state.json generated successfully for '{target_event['EventName']}' with {len(driver_pace)} drivers!")


if __name__ == "__main__":
    current_year = pd.Timestamp.now().year
    build_weekend_state(current_year)