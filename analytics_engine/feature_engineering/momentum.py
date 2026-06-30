import pandas as pd

def calculate_constructor_momentum(df):
    """Calculates a 5-race rolling average of points for each constructor."""
    
    # Sort chronologically
    df = df.sort_values(by=['season', 'round'])
    
    # Group by team and calculate rolling sum of points
    # We use a lambda to apply the rolling window to each team independently
    rolling_points = df.groupby('constructorId')['points'].transform(
        lambda x: x.rolling(window=5, min_periods=1).mean()
    )
    
    # CRITICAL ML RULE: Shift the data by 1!
    # The momentum GOING INTO the race cannot include the points scored IN the race.
    df['constructor_momentum_5_race'] = df.groupby('constructorId')['points'].transform(
        lambda x: x.rolling(window=5, min_periods=1).mean().shift(1)
    )
    
    # Fill NA values (for the first race of a team's history) with 0
    df['constructor_momentum_5_race'] = df['constructor_momentum_5_race'].fillna(0)
    
    return df