import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from pathlib import Path
import json

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_MATRIX_PATH = BASE_DIR / "data" / "processed" / "model_training_matrix.csv"
EXPORT_DIR = BASE_DIR.parent / "web_app" / "public" / "data"

MODEL_FEATURES = [
    'grid', 'driver_overall_avg', 'driver_track_avg', 'driver_street_avg',
    'team_momentum', 'driver_momentum', 'driver_racecraft_index',
    'tire_deg_index'
]

def run_evaluation():
    print("📊 Booting LapLogic Dual-Model Arena...")

    if not PROCESSED_MATRIX_PATH.exists():
        print(f"❌ Error: {PROCESSED_MATRIX_PATH} not found.")
        return

    df = pd.read_csv(PROCESSED_MATRIX_PATH)
    df = df.sort_values(by=['year', 'round'])

    # Time-Series Split
    train_df = df[df['year'] < 2024].copy()
    test_df = df[df['year'] >= 2024].copy()

    print(f"   -> Training on {len(train_df['raceId'].unique())} historical races...")
    
    # 1. Train Random Forest (The Reigning Champ)
    rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    rf.fit(train_df[MODEL_FEATURES], train_df['won_race'])

    # 2. Train XGBoost (The Challenger)
    # XGBoost excels at finding complex, non-linear relationships in tabular data
    xgb_model = xgb.XGBClassifier(
        n_estimators=200, 
        max_depth=4, 
        learning_rate=0.05, 
        objective='binary:logistic',
        eval_metric='logloss',
        random_state=42
    )
    xgb_model.fit(train_df[MODEL_FEATURES], train_df['won_race'])

    # Initialize scoreboards
    test_races = test_df['raceId'].unique()
    total_valid_races = 0
    
    baseline_wins = 0
    rf_wins, rf_podium_hits = 0, 0
    xgb_wins, xgb_podium_hits = 0, 0

    print(f"   -> Testing on {len(test_races)} unseen races (2024+)...")

    # Evaluate Race-by-Race
    for race_id in test_races:
        race_data = test_df[test_df['raceId'] == race_id].copy()
        
        if race_data['won_race'].sum() == 0:
            continue
            
        total_valid_races += 1
        true_winner = race_data[race_data['won_race'] == 1]['driverRef'].values[0]

        # Baseline
        baseline_pred = race_data.sort_values('grid')['driverRef'].values[0]
        if baseline_pred == true_winner:
            baseline_wins += 1

        # Random Forest Predictions
        race_data['rf_prob'] = rf.predict_proba(race_data[MODEL_FEATURES])[:, 1]
        rf_sorted = race_data.sort_values('rf_prob', ascending=False)
        if rf_sorted['driverRef'].values[0] == true_winner:
            rf_wins += 1
        if true_winner in rf_sorted['driverRef'].values[:3]:
            rf_podium_hits += 1

        # XGBoost Predictions
        race_data['xgb_prob'] = xgb_model.predict_proba(race_data[MODEL_FEATURES])[:, 1]
        xgb_sorted = race_data.sort_values('xgb_prob', ascending=False)
        if xgb_sorted['driverRef'].values[0] == true_winner:
            xgb_wins += 1
        if true_winner in xgb_sorted['driverRef'].values[:3]:
            xgb_podium_hits += 1

    # Calculate Final Percentages
    base_acc = (baseline_wins / total_valid_races) * 100
    rf_acc = (rf_wins / total_valid_races) * 100
    xgb_acc = (xgb_wins / total_valid_races) * 100
    
    rf_podium = (rf_podium_hits / total_valid_races) * 100
    xgb_podium = (xgb_podium_hits / total_valid_races) * 100

    # Determine the Champion
    champion = "XGBoost" if xgb_acc > rf_acc else "Random Forest"
    if xgb_acc == rf_acc:
        # Tie-breaker goes to podium coverage
        champion = "XGBoost" if xgb_podium > rf_podium else "Random Forest"

    print("\n" + "="*50)
    print("🏆 LAPLOGIC MODEL ARENA RESULTS")
    print("="*50)
    print(f"Grid Baseline:   {base_acc:.1f}%")
    print(f"Random Forest:   {rf_acc:.1f}% Win | {rf_podium:.1f}% Top-3")
    print(f"XGBoost:         {xgb_acc:.1f}% Win | {xgb_podium:.1f}% Top-3")
    print("-" * 50)
    print(f"👑 ACTIVE CHAMPION: {champion.upper()}")
    print("="*50 + "\n")

    # Export to JSON
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    metrics = {
        "totalRaces": total_valid_races,
        "baselineAccuracy": round(base_acc, 1),
        "champion": champion,
        "models": {
            "randomForest": {
                "winAccuracy": round(rf_acc, 1),
                "podiumCoverage": round(rf_podium, 1)
            },
            "xgBoost": {
                "winAccuracy": round(xgb_acc, 1),
                "podiumCoverage": round(xgb_podium, 1)
            }
        }
    }

    with open(EXPORT_DIR / "evaluation_metrics.json", 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    run_evaluation()