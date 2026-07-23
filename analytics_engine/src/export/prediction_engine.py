import json
import math
import pandas as pd
import fastf1
from pathlib import Path

EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"

def parse_laptime_str(time_str: str) -> float:
    """Converts M:SS.mmm string (e.g. '1:48.230') to total seconds."""
    try:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except Exception:
        return 0.0

def get_historical_momentum(current_year: int) -> dict:
    """Fallback helper: gets driver points over the last 3 completed races."""
    schedule = fastf1.get_event_schedule(current_year)
    now = pd.Timestamp.now().tz_localize(None)
    
    schedule['EventDate'] = pd.to_datetime(schedule['EventDate']).dt.tz_localize(None)
    past_races = schedule[schedule['EventDate'] < now].tail(3)
    
    momentum = {}
    for _, race in past_races.iterrows():
        try:
            session = fastf1.get_session(current_year, race['EventName'], 'R')
            session.load(telemetry=False, weather=False, messages=False)
            for _, driver in session.results.iterrows():
                d_id = str(driver['FullName']).lower().replace(' ', '_')
                momentum[d_id] = momentum.get(d_id, 0.0) + float(driver['Points'])
        except Exception:
            continue
    return momentum

def generate_predictions(current_year: int):
    print("🧠 Running LapLogic FP2-Enhanced Prediction Engine...")
    
    weekend_file = EXPORT_DIR / "weekend_state.json"
    fp2_pace_data = []
    
    # 1. Try loading FP2 Long Run Pace from weekend_state.json
    if weekend_file.exists():
        try:
            with open(weekend_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                fp2_pace_data = state.get("telemetry", {}).get("longRunPace", [])
        except Exception as e:
            print(f"   -> Warning reading weekend_state.json: {e}")

    predictions = []

    # 2. PATH A: We have FP2 Long-Run Pace Data
    if fp2_pace_data and len(fp2_pace_data) >= 3:
        print(f"   -> Found FP2 Pace Data for {len(fp2_pace_data)} drivers. Modeling long-run pace...")
        
        # Parse all average times into seconds
        parsed = []
        for item in fp2_pace_data:
            sec = parse_laptime_str(item.get("avgLapTime", ""))
            if sec > 0:
                parsed.append({
                    "driverId": item["driverId"],
                    "driverName": item["driverName"],
                    "seconds": sec
                })

        if parsed:
            # Find the benchmark (fastest average stint)
            fastest_time = min(p["seconds"] for p in parsed)
            
            # Convert lap time deltas to probability weights via exponential decay
            # Decay factor lambda = 1.5: a 1.0s/lap deficit drastically reduces win probability
            decay_factor = 1.5
            weights = []
            for p in parsed:
                delta = p["seconds"] - fastest_time
                weight = math.exp(-decay_factor * delta)
                weights.append(weight)
                
            total_weight = sum(weights) if sum(weights) > 0 else 1.0

            for i, p in enumerate(parsed):
                prob = weights[i] / total_weight
                predictions.append({
                    "driverId": p["driverId"],
                    "driverName": p["driverName"],
                    "winProbability": round(prob, 3),
                    "rawDelta": round(p["seconds"] - fastest_time, 3)
                })
                
            # Sort by highest win probability
            predictions.sort(key=lambda x: x["winProbability"], reverse=True)

    # 3. PATH B: Fallback to Historical Momentum (Pre-FP2 or off-season)
    if not predictions:
        print("   -> FP2 pace data unavailable or incomplete. Defaulting to 3-race Momentum model...")
        momentum = get_historical_momentum(current_year)
        total_momentum = sum(momentum.values()) if momentum else 1.0
        
        for driver_id, score in momentum.items():
            if score <= 0: continue
            name_formatted = " ".join([word.capitalize() for word in driver_id.split("_")])
            predictions.append({
                "driverId": driver_id,
                "driverName": name_formatted,
                "winProbability": round(score / total_momentum, 3),
                "rawDelta": 0.0
            })
        predictions.sort(key=lambda x: x["winProbability"], reverse=True)

    # 4. Format Top 10 Output for predictions.json
    final_output = []
    for i, pred in enumerate(predictions[:10]):
        final_output.append({
            "driverId": pred["driverId"],
            "driverName": pred["driverName"],
            "winProbability": pred["winProbability"],
            "predictedPosition": i + 1
        })

    # 5. Export JSON
    export_path = EXPORT_DIR / "predictions.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print("   -> predictions.json updated successfully!")