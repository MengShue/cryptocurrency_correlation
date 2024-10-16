from flask import Flask, jsonify, request, render_template
import yfinance as yf
import pandas as pd
from yahooquery import Screener
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DEFAULT_PERIOD = ['5d', '1mo', '3mo', '1y']
DEFAULT_INTERVAL = '1d'

# Route to render the frontend HTML
@app.route('/')
def index():
    return render_template('index.html')


# Route to get historical data for a cryptocurrency from Yahoo Finance
@app.route('/get_crypto_data', methods=['GET'])
def get_crypto_data():
    coin = request.args.get('coin', 'BTC-USD')
    period = request.args.get('period', '5d')

    if period not in DEFAULT_PERIOD:
        return jsonify({'error': 'Invalid period'}), 400

    if period in ['5d', '1mo']:
        interval = '1h'
    else:
        interval = DEFAULT_INTERVAL

    # Fetch data from Yahoo Finance
    data = yf.download(tickers=coin, period=period, interval=interval)

    # Convert to JSON
    data.reset_index(inplace=True)
    if interval == '1h':
        pd_date_name = 'Datetime'
    else:
        pd_date_name = 'Date'
    data[pd_date_name] = data[pd_date_name].astype(str)
    json_data = data[[pd_date_name, 'Close']].to_dict(orient='records')

    return jsonify(json_data)


# Route to get the list of available cryptocurrencies using Yahoo Finance API
@app.route('/get_coins', methods=['GET'])
def get_coins():
    s = Screener()
    data = s.get_screeners('all_cryptocurrencies_us', count=250)

    if 'quotes' not in data['all_cryptocurrencies_us']:
        return jsonify({'error': 'Failed to fetch coins list'}), 500

    # Extract symbols from the Yahoo Finance screener
    dicts = data['all_cryptocurrencies_us']['quotes']
    symbols = sorted([d['symbol'] for d in dicts])
    symbols.remove("BTC-USD")
    symbols.remove("ETH-USD")

    return jsonify(symbols)


# Route to get historical data for BTC and another coin, and calculate correlation
@app.route('/get_crypto_data_and_correlation', methods=['GET'])
def get_crypto_data_and_correlation():
    coin = request.args.get('coin', 'ETH-USD')  # Default second coin is ETH-USD
    period = request.args.get('period', '1mo')  # Default period is 1 month

    if period not in ['5d', '1mo', '3mo', '1y']:
        return jsonify({'error': 'Invalid period'}), 400

    if period in ['5d', '1mo']:
        interval = '1h'
    else:
        interval = DEFAULT_INTERVAL

    # Fetch BTC and the selected coin data
    btc_data = yf.download(tickers='BTC-USD', period=period, interval=interval)
    alt_data = yf.download(tickers=coin, period=period, interval=interval)

    # Reset index and keep only the 'Close' and 'Date' columns
    btc_data.reset_index(inplace=True)
    alt_data.reset_index(inplace=True)
    if interval == '1h':
        pd_date_name = 'Datetime'
    else:
        pd_date_name = 'Date'
    btc_data = btc_data[[pd_date_name, 'Close']]
    alt_data = alt_data[[pd_date_name, 'Close']]

    # Merge the two datasets on the 'Date' column
    merged_data = pd.merge(btc_data, alt_data, on=pd_date_name, suffixes=('_BTC', f'_{coin.split("-")[0]}'))

    # Calculate correlation between BTC and the selected coin
    correlation = merged_data['Close_BTC'].corr(merged_data[f'Close_{coin.split("-")[0]}'])

    # Convert to JSON for the frontend
    merged_data[pd_date_name] = merged_data[pd_date_name].astype(str)  # Convert date to string
    json_data = merged_data.to_dict(orient='records')

    return jsonify({
        'data': json_data,
        'correlation': correlation
    })


if __name__ == '__main__':
    app.run(debug=True)