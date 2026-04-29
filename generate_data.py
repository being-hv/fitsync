import numpy as np
import pandas as pd
from datetime import timedelta, datetime

# Initialize parameters
num_days = 365
date_start = datetime(2025, 1, 1)

def generate_fitness_data(num_days):
    dates = [date_start + timedelta(days=i) for i in range(num_days)]
    steps = np.random.normal(loc=8500, scale=2500, size=num_days).clip(3000, 18000)
    sleep_hours = np.random.normal(loc=7.2, scale=1, size=num_days).clip(4.5, 9.5)
    sleep_score = np.random.randint(60, 100, size=num_days)
    heart_rate_bpm = np.random.normal(loc=68, scale=10, size=num_days).clip(48, 110)
    calories_burned = np.random.randint(1800, 4200, size=num_days)
    active_minutes = np.random.randint(20, 180, size=num_days)

    # Introduce 5% missing values in each column
    data = {
        'date': dates,
        'steps': steps,
        'sleep_hours': sleep_hours,
        'sleep_score': sleep_score,
        'heart_rate_bpm': heart_rate_bpm,
        'calories_burned': calories_burned,
        'active_minutes': active_minutes
    }

    df = pd.DataFrame(data)
    for column in df.columns[1:]:  # Skip 'date'
        df.loc[df.sample(frac=0.05).index, column] = np.nan

    return df

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Generate and save the data
df = generate_fitness_data(num_days)
save_to_csv(df, 'data/health.csv')
