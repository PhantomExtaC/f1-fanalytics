import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

EXPORT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "web_app" / "public" / "data"

def parse_laptime_str(time_str: str) -> float:
    try:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except Exception:
        return 0.0

def get_training_data():
    """
    In production, this queries your historical database. 
    For now, this is the schema the Random Forest needs to learn 
    the interactions between Track Temp, Pit Delta, and FP2 Pace.
    """
    # Features: [Track_Temp, Pit_Delta, FP2_Pace_Deficit_To_Leader]
    # Target: 1 (Won the race) or 0 (Did not win)
    data = {
        "track_temp": [35.0, 42.0, 22.0, 25.0, 45.0, 30.0],
        "pit_delta":  [20.5, 24.0, 16.0, 19.5, 22.0, 18.0],
        "fp2_deficit": [0.0, 0.4, 0.1, 1.2, 0.0, 0.5],
        "won_race":    [1, 0, 1, 0, 1, 0] 
    }
    return pd.DataFrame(data)

def run_rf_predictions():
    print("🌲 Booting LapLogic Random Forest Engine...")

    # 1. Train the Model
    df_train = get_training_data()
    X_train = df_train[["track_temp", "pit_delta", "fp2_deficit"]]
    y_train = df_train["won_race"]

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    print("   -> Model trained on historical multi-variable data.")

    # 2. Load Current Weekend State
    weekend_file = EXPORT_DIR / "weekend_state.json"
    if not weekend_file.exists():
        print("   -> Error: weekend_state.json not found. Run weekend_builder.py first.")
        return

    with open(weekend_file, 'r', encoding='utf-8') as f:
        state = json.load(f)

    track_temp = state.get("weather", {}).get("trackTemp", 30.0)
    pit_delta = state.get("track", {}).get("pitStopDelta", 20.0)
    fp2_data = state.get("telemetry", {}).get("longRunPace", [])

    if not fp2_data:
        print("   -> Error: No FP2 data available in weekend_state.json to make RF predictions.")
        return

    # 3. Prepare Live Features
    parsed = []
    for item in fp2_data:
        sec = parse_laptime_str(item.get("avgLapTime", ""))
        if sec > 0:
            parsed.append({"driverId": item["driverId"], "driverName": item["driverName"], "seconds": sec})

    fastest_time = min(p["seconds"] for p in parsed)
    
    live_features = []
    for p in parsed:
        deficit = p["seconds"] - fastest_time
        live_features.append([track_temp, pit_delta, deficit])

    X_live = pd.DataFrame(live_features, columns=["track_temp", "pit_delta", "fp2_deficit"])

    # 4. Predict Probabilities
    # .predict_proba returns an array like [Prob_Loss, Prob_Win]
    probabilities = model.predict_proba(X_live)[:, 1] 

    predictions = []
    for i, p in enumerate(parsed):
        predictions.append({
            "driverId": p["driverId"],
            "driverName": p["driverName"],
            "winProbability": round(float(probabilities[i]), 3)
        })

    # Normalize probabilities so they equal 100% (1.0)
    total_prob = sum(pred["winProbability"] for pred in predictions)
    if total_prob > 0:
        for pred in predictions:
            pred["winProbability"] = round(pred["winProbability"] / total_prob, 3)

    # Sort by highest probability
    predictions.sort(key=lambda x: x["winProbability"], reverse=True)

    # 5. Format and Overwrite predictions.json
    final_output = []
    for i, pred in enumerate(predictions[:10]):
        final_output.append({
            "driverId": pred["driverId"],
            "driverName": pred["driverName"],
            "winProbability": pred["winProbability"],
            "predictedPosition": i + 1
        })

    export_path = EXPORT_DIR / "predictions.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("   -> predictions.json overwritten with Random Forest inferences!")

if __name__ == "__main__":
    run_rf_predictions()