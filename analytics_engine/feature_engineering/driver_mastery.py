import pandas as pd

def calculate_hierarchical_track_mastery(df):
    """
    Calculates driver baseline expectations using dynamic sequential lookbacks.
    
    Features engineered:
      - driver_overall_avg: Historical average finish across all tracks up to this race.
      - driver_track_avg: Historical track-specific average finish up to this race.
    """
    # Enforce strict chronological progression so features look backward only
    df = df.sort_values(by=['season', 'round']).reset_index(drop=True)
    
    # 1. Career average at this point in time (all tracks)
    df['driver_overall_avg'] = df.groupby('driverId')['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 2. Track-specific historical average up to this point in time
    df['driver_track_avg'] = df.groupby(['driverId', 'circuitId'])['positionOrder'].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # 3. Dynamic Imputation: Fallback to general career average if track-newcomer
    # This captures driver skill instantly without watering everyone down to a 10.0
    df['driver_track_avg'] = df['driver_track_avg'].fillna(df['driver_overall_avg'])
    
    # 4. Ultimate Rookie Safety Gate
    # If it is their literal first race in F1 career, fallback to grid midpoint
    df['driver_track_avg'] = df['driver_track_avg'].fillna(10.5)
    df['driver_overall_avg'] = df['driver_overall_avg'].fillna(10.5)
    
    return df

# Analytical Insight Check
if __name__ == "__main__":
    # Small test mockup tracking a driver's career progression
    mock_data = pd.DataFrame([
        {'season': 2024, 'round': 1, 'driverId': 'piastri', 'circuitId': 'bahrain', 'positionOrder': 8},
        {'season': 2024, 'round': 2, 'driverId': 'piastri', 'circuitId': 'jeddah', 'positionOrder': 4},
        {'season': 2024, 'round': 3, 'driverId': 'piastri', 'circuitId': 'bahrain', 'positionOrder': 2},
    ])
    
    output = calculate_hierarchical_track_mastery(mock_data)
    print("\n--- Feature Engineering Output Preview ---")
    print(output[['season', 'round', 'circuitId', 'driver_overall_avg', 'driver_track_avg']])