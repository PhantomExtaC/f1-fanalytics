import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_MATRIX_PATH = BASE_DIR / "data" / "processed" / "model_training_matrix.csv"
FEATURES_DIR = BASE_DIR / "data" / "features"
EXPORT_DIR = BASE_DIR.parent / "web_app" / "public" / "data"

# Consistent feature list used for both Training and Inference
MODEL_FEATURES = [
    'grid',
    'driver_overall_avg',
    'driver_track_avg',
    'driver_street_avg',
    'team_momentum',
    'driver_momentum',
    'driver_racecraft_index',
    'tire_deg_index',
    'is_street'
]



def run_rf_predictions():
    print("🌲 Booting LapLogic Random Forest Engine...")

    # 0. Verify and Load Training Matrix
    if not PROCESSED_MATRIX_PATH.exists():
        print(f"❌ Error: {PROCESSED_MATRIX_PATH} not found. Run build_dataset.py first!")
        return

    # 1. Train the Model
    df_train = pd.read_csv(PROCESSED_MATRIX_PATH)
    X_train = df_train[MODEL_FEATURES]
    y_train = df_train["won_race"]

    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    print(f"   -> Model trained on {len(df_train)} historical samples across {len(MODEL_FEATURES)} features.")

    # 2. Load Current Weekend Context
    weekend_file = EXPORT_DIR / "weekend_state.json"
    upcoming_drivers = []
    
    if weekend_file.exists():
        with open(weekend_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            long_runs = state.get("telemetry", {}).get("longRunPace", [])
            upcoming_drivers = [item["driverId"] for item in long_runs]

    # Fallback list of modern grid drivers if weekend_state.json is empty
    if not upcoming_drivers:
        upcoming_drivers = [
            "max_verstappen", "lando_norris", "charles_leclerc", "oscar_piastri",
            "lewis_hamilton", "george_russell", "carlos_sainz", "fernando_alonso"
        ]

    # 3. Pull latest features for upcoming drivers from data/features/
    df_mastery = pd.read_csv(FEATURES_DIR / "mastery_matrix.csv")
    df_power = pd.read_csv(FEATURES_DIR / "power_ratings.csv")
    df_track = pd.read_csv(FEATURES_DIR / "track_profiles.csv")

    latest_mastery = df_mastery.sort_values("raceId").groupby("driverRef").last().reset_index()
    latest_power = df_power.sort_values("raceId").groupby("driverRef").last().reset_index()
    latest_track = df_track.iloc[0]

    # Map FastF1 3-letter codes to Ergast full references
    DRIVER_MAP = {
        "ver": "max_verstappen", "per": "perez",
        "ham": "hamilton", "rus": "russell",
        "lec": "leclerc", "sai": "sainz",
        "nor": "norris", "pia": "piastri",
        "alo": "alonso", "str": "stroll",
        "gas": "gasly", "oco": "ocon", "doo": "doohan",
        "alb": "albon", "col": "colapinto", "sar": "sargeant",
        "tsu": "tsunoda", "law": "lawson", "ric": "ricciardo",
        "bot": "bottas", "zho": "zhou",
        "hul": "hulkenberg", "mag": "magnussen", "bea": "bearman",
        "ant": "antonelli", "had": "hadjar", "bor": "bortoleto"
    }

    live_rows = []
    for i, d_ref in enumerate(upcoming_drivers):
        # Translate 'hul' to 'hulkenberg'
        ergast_ref = DRIVER_MAP.get(d_ref.lower(), d_ref.lower())
    
        m_row = latest_mastery[latest_mastery['driverRef'] == ergast_ref]
        p_row = latest_power[latest_power['driverRef'] == ergast_ref]

        live_rows.append({
            'driverId': d_ref.lower(),
            'driverName': d_ref.upper(),
            'grid': i + 1,
            'driver_overall_avg': m_row['driver_overall_avg'].values[0] if not m_row.empty else 5.0,
            'driver_track_avg': m_row['driver_track_avg'].values[0] if not m_row.empty else 5.0,
            'driver_street_avg': m_row['driver_street_avg'].values[0] if not m_row.empty else 5.0,
            'team_momentum': p_row['team_momentum'].values[0] if not p_row.empty else 0.0,
            'driver_momentum': p_row['driver_momentum'].values[0] if not p_row.empty else 5.0,
            'driver_racecraft_index': p_row['driver_racecraft_index'].values[0] if not p_row.empty else 0.0,
            'tire_deg_index': latest_track['tire_deg_index']
        })

    df_live = pd.DataFrame(live_rows)

    # 4. Predict Win Probabilities
    X_live = df_live[MODEL_FEATURES]
    probs = model.predict_proba(X_live)[:, 1]

    for i, prob in enumerate(probs):
        live_rows[i]['winProbability'] = float(prob)

    # Normalize probabilities to 1.0 (100%)
    total_prob = sum(r['winProbability'] for r in live_rows)
    if total_prob > 0:
        for r in live_rows:
            r['winProbability'] = round(r['winProbability'] / total_prob, 3)

    # Sort descending by win probability
    live_rows.sort(key=lambda x: x['winProbability'], reverse=True)

    # 5. Format Top 10 for React UI
    # 5. Format Top 10 for React UI
    final_output = []
    for i, item in enumerate(live_rows[:10]):
        final_output.append({
            "driverId": item["driverId"],
            "driverName": item["driverName"],
            "winProbability": item["winProbability"],
            "predictedPosition": i + 1,
            "insights": {
                "trackMastery": round(float(item["driver_track_avg"]), 1),
                "teamMomentum": round(float(item["team_momentum"]), 1),
                "driverMomentum": round(float(item["driver_momentum"]), 1)
            }
        })

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = EXPORT_DIR / "predictions.json"
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"✅ predictions.json updated with Random Forest predictions at {export_path}")

if __name__ == "__main__":
    run_rf_predictions()