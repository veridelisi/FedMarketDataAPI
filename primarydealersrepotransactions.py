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

import pandas as pd
import requests
from io import StringIO

# URL of the data definitions CSV file
data_definitions_url = "https://markets.newyorkfed.org/api/pd/list/timeseries.csv"

# Make the request to download the data definitions file
response_definitions = requests.get(data_definitions_url)

# Check if the request was successful
if response_definitions.status_code == 200:
    # Load the content of the response into a DataFrame
    data_definitions = pd.read_csv(StringIO(response_definitions.text))
    print(data_definitions.head())  # Display the first few rows of the DataFrame
else:
    print(f"Failed to download the data definitions file: {response_definitions.status_code}")


# Filter the DataFrame for rows containing "Repurchase Agreements" in the "Label" column
repurchase_agreements_rows = data_definitions[data_definitions['Label'].str.contains("Repurchase Agreements", na=False)]

print(repurchase_agreements_rows)


# Joining the two DataFrames
merged_data = pd.merge(filtered_data, repurchase_agreements_rows, left_on='Time Series', right_on='Key Id')

# Displaying the merged DataFrame

merged_data

# Assuming you have a column that contains the phrase "Repurchase Agreements"
# Replace 'column_name' with the actual name of the column

filtered_repurchase_agreements = merged_data[merged_data['Label'].str.startswith('Repurchase Agreements')]

# Display the filtered DataFrame
filtered_repurchase_agreements

# Assuming filtered_repurchase_agreements is the DataFrame that we want to save as an Excel file
# Save the DataFrame to an Excel file in the writable filesystem of the environment
excel_filepath = 'filtered_repurchase_agreements.xlsx'
filtered_repurchase_agreements.to_excel(excel_filepath, index=False)

# Provide the path for download
excel_filepath



