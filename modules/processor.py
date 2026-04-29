import pandas as pd


def load_data():
    """
    Load health data CSV, handle missing values, and convert date column.
    """
    
    # Read the CSV file from the data directory
    df = pd.read_csv('data/health_data.csv')
    
    # Handle missing values intelligently
    # Fill missing steps with median value of the steps column
    df['steps'].fillna(df['steps'].median(), inplace=True)
    
    # Fill missing sleep_hours with 7.0
    df['sleep_hours'].fillna(7.0, inplace=True)
    
    # Fill missing heart_rate_bpm with 68
    df['heart_rate_bpm'].fillna(68, inplace=True)
    
    # Fill other columns with their median values
    for column in df.columns:
        if df[column].isnull().any():
            df[column].fillna(df[column].median(), inplace=True)
    
    # Convert the 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    # Return the cleaned DataFrame
    return df


def calculate_recovery_score(df):
    """
    Calculate the Recovery Score for each entry in the DataFrame.
    Adds a new column 'Recovery_Score' with values ranging from 0 to 100, representing
    the body's recovery level for the day based on sleep, heart rate, and physical activity.
    """
    recovery_scores = []

    for _, row in df.iterrows():
        sleep_score = 0
        heart_rate_score = 0
        steps_score = 0

        # Determine sleep score based on sleep_hours
        if row['sleep_hours'] >= 7:
            sleep_score = 40  # Good sleep boosts score
        elif row['sleep_hours'] < 6:
            sleep_score = -20  # Poor sleep decreases score
        else:
            sleep_score = 20  # Average sleep provides moderate boost

        # Determine heart rate score based on heart_rate_bpm
        if row['heart_rate_bpm'] < 60:
            heart_rate_score = 30  # Lower resting heart rate is beneficial
        elif row['heart_rate_bpm'] < 75:
            heart_rate_score = 15  # Moderate heart rate gives small boost
        else:
            heart_rate_score = 0  # High resting heart rate does not affect positively

        # Determine steps score based on steps
        if row['steps'] > 12000:
            steps_score = -10  # Very high activity could be straining
        elif row['steps'] > 8000:
            steps_score = 20  # Good activity level enhances recovery
        else:
            steps_score = 0  # Low activity level gets no bonus

        # Calculate total score and ensure it's within the 0 to 100 range
        total_score = sleep_score + heart_rate_score + steps_score
        total_score = max(0, min(100, total_score))

        recovery_scores.append(total_score)

    # Add the new Recovery_Score column to the DataFrame
    df['Recovery_Score'] = recovery_scores

    return df


def process_data():
    """
    Main function to process health data for the Streamlit dashboard.

    Returns:
        pd.DataFrame: The processed DataFrame with recovery scores.
    """
    # Load the data
    df = load_data()

    # Calculate and add Recovery Score
    df = calculate_recovery_score(df)

    # Return the processed DataFrame
    return df

