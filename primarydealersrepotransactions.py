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
#filtered_repurchase_agreements

# Assuming 'filtered_repurchase_agreements' is your DataFrame
# Remove "Repurchase Agreements:" from each row in the "Label" column
filtered_repurchase_agreements['Label'] = filtered_repurchase_agreements['Label'].str.replace("Repurchase Agreements:", "")

# Now the "Label" column should have the "Repurchase Agreements:" statement removed from every row
print(filtered_repurchase_agreements['Label'])


import pandas as pd
import numpy as np

# Your DataFrame is named filtered_repurchase_agreements
# Define the pattern to match the different categories
pattern = (
    r"(U.S. Treasury securities \(excluding TIPS\) -|"
    r"U.S. Treasury Inflation-Protected Securities \(TIPS\) -|"
    r"Federal Agency and GSE Residential MBS -|"
    r"Federal Agency and GSE CMBS -|"
    r"Corporate Debt -|"
    r"Asset-backed securities -|"
    r"Equities -|"
    r"Other -|"
    r"Federal Agency and GSE Securities \(excluding MBS\) -)"
)

# Extract the matching text into a new column 'label1'
filtered_repurchase_agreements['label1'] = filtered_repurchase_agreements['Label'].str.extract(pattern)

# Replace NaN with an empty string or any other placeholder if needed
filtered_repurchase_agreements['label1'] = filtered_repurchase_agreements['label1'].replace(np.nan, '')

# Display the DataFrame to verify the changes
filtered_repurchase_agreements



# Define the pattern to match the different categories
pattern_to_remove = (
    r"U.S. Treasury securities \(excluding TIPS\) -|"
    r"U.S. Treasury Inflation-Protected Securities \(TIPS\) -|"
    r"Federal Agency and GSE Residential MBS -|"
    r"Federal Agency and GSE CMBS -|"
    r"Corporate Debt -|"
    r"Asset-backed securities -|"
    r"Equities -|"
    r"Other -|"
    r"Federal Agency and GSE Securities \(excluding MBS\) -"
)

# Remove the matched text from the 'Label' column
filtered_repurchase_agreements['Label'] = filtered_repurchase_agreements['Label'].str.replace(pattern_to_remove, "", regex=True)

# Display the DataFrame to verify the changes
filtered_repurchase_agreements


# Define the pattern with capture groups to match the desired expressions for label2
# Define the pattern with a non-capturing group to match the desired expressions for label2
pattern_label2 = (
    r"(Cleared Bilateral|"
    r"Uncleared Bilateral|"
    r"GCF|"
    r"Triparty \(excluding GCF\) )"
)

# Extract the matching text into a new column 'label2'
# The 'expand=False' parameter tells pandas to return a Series, which ensures a single column
filtered_repurchase_agreements['label2'] = filtered_repurchase_agreements['Label'].str.extract(pattern_label2, expand=False)

# Replace NaN with an empty string or any other placeholder if needed
filtered_repurchase_agreements['label2'] = filtered_repurchase_agreements['label2'].replace(np.nan, '')

# Display the DataFrame to verify the changes
filtered_repurchase_agreements


# Define the pattern to match the expressions to be removed
pattern_label2 = (
    r"Cleared Bilateral|"
    r"Uncleared Bilateral|"
    r"GCF|"
    r"Triparty \(excluding GCF\) "
)

# Remove the matched text from the 'Label' column
filtered_repurchase_agreements['Label'] = filtered_repurchase_agreements['Label'].str.replace(pattern_label2, "", regex=True)

# Display the DataFrame to verify the changes
filtered_repurchase_agreements


# Sample data creation for demonstration
# Let's assume filtered_repurchase_agreements is your DataFrame and it looks like this:
# filtered_repurchase_agreements = pd.DataFrame({
#     'label1': ['U.S. Treasury securities (excluding TIPS) -', 'U.S. Treasury Inflation-Protected Securities (TIPS) -'],
#     'Value (millions)': ['66284683379843182764808442509*2316039994', '123456789*987654321']
# })

# Step 1: Split the 'Value (millions)' column by asterisk and expand into separate columns
split_values = filtered_repurchase_agreements['Value (millions)'].str.split('*', expand=True)

# Step 2: Convert the split strings into numbers and sum them row-wise
# Make sure all values are converted to numbers, here we use pandas.to_numeric with errors='coerce' to handle non-numeric values
split_values = split_values.apply(pd.to_numeric, errors='coerce')

# Add a new column to the existing DataFrame that contains the sum of the numeric values
filtered_repurchase_agreements['Sum of Values'] = split_values.sum(axis=1)

# Now, if you want to sum these values for each category in 'label1'
category_sums = filtered_repurchase_agreements.groupby('label1')['Sum of Values'].sum()

# Display the resulting sums for each category
category_sums


# Use the pivot_table function to create the desired summary
pivot_table = filtered_repurchase_agreements.pivot_table(
    index='label1',  # Rows (index) will be labeled by unique values from 'label1'
    columns='label2',  # Columns will be labeled by unique values from 'label2'
    values='Sum of Values',  # The cell values are the sums from 'Sum of Values'
    aggfunc='sum'  # Use the sum function to aggregate
).fillna(0)  # Fill any NaN values with 0




pivot_table
