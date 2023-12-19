import pandas as pd
import requests
from io import StringIO

# URL of the CSV file
url = "https://markets.newyorkfed.org/api/pd/get/all/timeseries.csv"

# Make the request to download the file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use StringIO to read the CSV text into a DataFrame
    data = pd.read_csv(StringIO(response.text))
    print(data.describe())  # Display the first few rows of the DataFrame
else:
    print(f"Failed to download the file: {response.status_code}")

    print(f"Failed to download the file: {response.status_code}")

# Convert the date column to datetime if it's not already
data['As Of Date'] = pd.to_datetime(data['As Of Date'])

# Filter the DataFrame for the specific date
filtered_data = data[data['As Of Date'] == '2023-12-06']

# Display the filtered DataFrame
print(filtered_data)
