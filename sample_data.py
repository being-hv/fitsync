import pandas as pd

# Load the health_data.csv file from the data directory
file_path = 'data/health_data.csv'
data = pd.read_csv(file_path)

# Print the first 5 rows of the dataframe
print('First 5 rows:')
print(data.head())

# Calculate the number of missing values in each column
missing_values = data.isnull().sum()

# Print the number of missing values per column
print('\nNumber of missing values in each column:')
print(missing_values)