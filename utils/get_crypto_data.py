import requests
import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import io
import json

COINS_FILE = 'coins.json'

def is_valid_coin(coin_symbol):
    """
    Checks if a coin symbol is valid by looking it up in the local coin list.
    """
    try:
        with open(COINS_FILE, 'r') as f:
            coins = json.load(f)
    except FileNotFoundError:
        return False  # If the coin list doesn't exist, all coins are considered invalid

    for coin in coins:
        if coin['symbol'].upper() == coin_symbol.upper():
            return True
    return False

# Function to get metadata for a coin (includes logo)
def get_crypto_metadata(coin_symbol):
    if not is_valid_coin(coin_symbol):
        return None
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
    }
    params = {
        "symbol": coin_symbol.upper(),
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get crypto data for a specific coin
def get_crypto_data(coin_symbol):
    if not is_valid_coin(coin_symbol):
        return None
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY"),
    }
    params = {
        "symbol": coin_symbol.upper(),
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get historical data using Binance API
def get_historical_data_binance_df(coin_symbol, interval='1d', limit='30'):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": f"{coin_symbol.upper()}USDT",  # e.g., BTCUSDT
        "interval": interval,  # Time interval for data, e.g., '1d', '15m', etc.
        "limit": limit  # Number of data points to retrieve
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extract the relevant OHLCV data (Open, High, Low, Close, Volume)
        return [{
            "time": int(item[0]),
            "open": float(item[1]),
            "high": float(item[2]),
            "low": float(item[3]),
            "close": float(item[4]),
            "volume": float(item[5])
        } for item in data]
    return None

# Function to get historical data using CoinGecko as a fallback
def get_historical_data_coingecko(coin_symbol, days='30'):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_symbol}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,  # Can be '1', '7', '30', etc.
        "interval": "daily"  # Can be 'hourly' or 'daily'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "prices" in data:
            return [{
                "time": int(price[0]),
                "close": float(price[1])
            } for price in data["prices"]]
    return None

# Function to get historical data from Binance for EMA calculations
def get_historical_data_binance(coin_symbol, interval='1d', limit='100'):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": f"{coin_symbol.upper()}USDT",  # e.g., BTCUSDT
        "interval": interval,  # Interval (e.g., '1h', '4h', '12h', '1d')
        "limit": limit  # Number of data points (e.g., last 100 intervals)
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])
        df['close'] = df['close'].astype(float)
        return df
    return None

# Function to calculate EMA and RSI indicators
def calculate_indicators(df):
    # Calculate 12-period EMA, 26-period EMA, 100-period EMA, 200-period EMA
    df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA_200'] = df['close'].ewm(span=200, adjust=False).mean()

    # Calculate RSI (14-period) with protection against division by zero
    delta = df['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    # Add a small epsilon to avoid division by zero
    rs = avg_gain / (avg_loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Calculate MACD and MACD Signal Line
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

# Function to perform ARIMA forecast
def arima_forecast(df, forecast_periods=5):
    # Ensure we have enough data
    if len(df) < 30:
        return None, "Not enough historical data to make a reliable forecast."

    # Use the 'close' price for forecasting
    model = ARIMA(df['close'], order=(5,1,0))
    model_fit = model.fit()

    # Forecast the next periods
    forecast = model_fit.forecast(steps=forecast_periods)
    return forecast, None

# Function to generate a forecast chart
def generate_forecast_chart(df, forecast, coin_symbol, interval):
    plt.figure(figsize=(10, 6))
    plt.plot(df['close'], label='Historical Close Price')
    plt.plot(forecast, label='ARIMA Forecast', linestyle='--')
    plt.title(f'{coin_symbol.upper()} Price Forecast ({interval})')
    plt.xlabel('Time')
    plt.ylabel('Price (USDT)')
    plt.legend()
    plt.grid(True)

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf
