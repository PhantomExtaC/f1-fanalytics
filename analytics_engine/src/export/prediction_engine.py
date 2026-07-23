import fastf1
import pandas as pd
import json
from pathlib import Path

# Target the React public directory
EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"

def generate_predictions(current_year: int):
    print("🧠 Booting LapLogic Prediction Engine...")
    
    schedule = fastf1.get_event_schedule(current_year)
    now = pd.Timestamp.now()
    
    # 1. Identify the upcoming race and the last 3 completed races
    # Drop timezones for safe comparison
    schedule['EventDate'] = pd.to_datetime(schedule['EventDate']).dt.tz_localize(None)
    
    past_races = schedule[schedule['EventDate'] < now].tail(3) 
    upcoming = schedule[schedule['EventDate'] >= now]
    
    if upcoming.empty:
        print("   -> Season completed. No predictions generated.")
        return
        
    next_race = upcoming.iloc[0]
    print(f"   -> Targeting Next Grand Prix: {next_race['EventName']}")
    
    # 2. Calculate Driver Momentum
    momentum_scores = {}
    names_map = {}
    
    for _, race in past_races.iterrows():
        try:
            # Load the race session (telemetry=False saves massive load times)
            session = fastf1.get_session(current_year, race['EventName'], 'R')
            session.load(telemetry=False, weather=False, messages=False)
            
            for _, driver in session.results.iterrows():
                name = str(driver['FullName'])
                driver_id = name.lower().replace(' ', '_')
                points = float(driver['Points'])
                
                momentum_scores[driver_id] = momentum_scores.get(driver_id, 0) + points
                names_map[driver_id] = name
        except Exception as e:
            print(f"   -> Skipping {race['EventName']} due to load error: {e}")
            continue
            
    # 3. Calculate Probabilities
    # The total points scored over the last 3 races acts as our denominator
    total_momentum = sum(momentum_scores.values()) if momentum_scores else 1
    
    predictions = []
    for driver_id, score in momentum_scores.items():
        if score == 0: continue # Exclude drivers with 0 momentum
        
        prob = score / total_momentum
        predictions.append({
            "driverId": driver_id,
            "driverName": names_map[driver_id],
            "winProbability": round(prob, 3),
            "rawScore": score
        })
        
    # Sort by highest probability
    predictions.sort(key=lambda x: x['rawScore'], reverse=True)
    
    # 4. Format for the React Frontend (Top 10)
    final_output = []
    for i, pred in enumerate(predictions[:10]):
        final_output.append({
            "driverId": pred['driverId'],
            "driverName": pred['driverName'],
            "winProbability": pred['winProbability'],
            "predictedPosition": i + 1
        })
        
    # 5. Export to JSON
    export_path = EXPORT_DIR / "predictions.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print("   -> predictions.json generated successfully!")