# Cryptocurrency Correlation App

This web application allows you to visualize the price of Bitcoin (BTC) and another selected cryptocurrency, calculate the correlation between their prices, and display it. The data is fetched from Yahoo Finance using the `yahooquery` and `yfinance` libraries.

## Features

- Visualize the price of Bitcoin (BTC) and another selected cryptocurrency.
- Calculate and display the correlation between BTC and the selected coin.
- Select time periods: 5 days, 1 month, 3 months, and 1 year.
- Cryptocurrency selection from a dropdown menu, sorted alphabetically.

## Requirements

- Python 3.x
- Flask
- pandas
- yfinance
- flask-cors
- yahooquery

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:MengShue/cryptocurrency_correlation.git
   cd cryptocurrency_correlation
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
## Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and go to:
   ```bash
   http://127.0.0.1:5000/
   ```
   
## Usage

- Select a cryptocurrency from the dropdown menu.
- Choose a time period (5 days, 1 month, 3 months, or 1 year).
- The application will plot the prices of Bitcoin (BTC) and the selected cryptocurrency.
- The correlation between BTC and the selected cryptocurrency will be displayed below the chart.

## Disclaimer
This application assumes that if a cryptocurrency shows a significant positive correlation with Bitcoin (BTC), it is considered to be following the trend of Bitcoin, the "gold standard" of cryptocurrencies. If there is no such correlation, it may indicate that the cryptocurrency lacks market traction. However, this is merely an assumption and does not constitute investment advice.
