# Primary Dealers Repo Transactions Volume Analysis

## Overview
This repository contains analysis of the repo transactions conducted by primary dealers in various securities across different types of repo agreements. The analysis focuses on understanding the volume of transactions, categorized by the type of security and the repo agreement.

## Data Source
The data used in this analysis is sourced from the New York Federal Reserve Market Data API. More information about the API and how to use it can be found in the official documentation: [NY Fed Markets API](https://markets.newyorkfed.org/static/docs/markets-api.html).

## Repository Contents
- `PrimaryDealersRepoTransactionsVolume.ipynb`: Jupyter notebook containing the data analysis, including data acquisition, processing, and summarization.

## Calculations
The calculations performed in the Jupyter notebook include:
- Grouping the repo transaction data by security type (`label1`) and repo agreement (`label2`).
- Summing up the transaction volumes for each unique combination of security type and repo agreement.
- Presenting the summed volumes in a pivot table format for easy comparison and analysis.

The analysis helps in identifying the transaction volumes associated with different securities and repo agreements, offering insights into market behaviors and dealer activities.

## Results
The results of the analysis are summarized in the Jupyter notebook, which can be viewed directly on GitHub: [Primary Dealers Repo Transactions Volume](https://github.com/veridelisi/FedMarketDataAPI/blob/main/PrimaryDealersRepoTransactionsVolume.ipynb).

## How to Use
To replicate the analysis or to perform your own analysis with the latest data:
1. Clone the repository to your local machine.
2. Ensure you have Jupyter Notebook or JupyterLab installed, along with Pandas and other required libraries.
3. Obtain an API key from the NY Fed Markets API if necessary.
4. Run the notebook `PrimaryDealersRepoTransactionsVolume.ipynb` to see the analysis steps and modify as required for your own analysis.

## Contributions
Contributions to this analysis are welcome. Please open an issue or submit a pull request if you have suggestions or improvements.

## License
The content of this repository is licensed under [MIT License](LICENSE), unless otherwise specified.

---
*This README is a brief overview of the analysis conducted. For any questions or additional information, feel free to open an issue.*
