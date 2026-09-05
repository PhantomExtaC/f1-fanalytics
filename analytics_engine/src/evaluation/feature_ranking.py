import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_MATRIX_PATH = BASE_DIR / "data" / "processed" / "model_training_matrix.csv"

MODEL_FEATURES = [
    'grid', 'driver_overall_avg', 'driver_track_avg', 'driver_street_avg',
    'team_momentum', 'driver_momentum', 'driver_racecraft_index',
    'tire_deg_index'
]

df = pd.read_csv(PROCESSED_MATRIX_PATH)
train_df = df[df['year'] < 2024].copy()

# 1. Random Forest Feature Importance
rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
rf.fit(train_df[MODEL_FEATURES], train_df['won_race'])

# 2. XGBoost Feature Importance
xgb_model = xgb.XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42)
xgb_model.fit(train_df[MODEL_FEATURES], train_df['won_race'])

importance_df = pd.DataFrame({
    'Feature': MODEL_FEATURES,
    'RF_Importance (%)': (rf.feature_importances_ * 100).round(2),
    'XGB_Importance (%)': (xgb_model.feature_importances_ * 100).round(2)
}).sort_values(by='RF_Importance (%)', ascending=False)

print("\n--- FEATURE IMPORTANCE BREAKDOWN ---")
print(importance_df.to_string(index=False))