import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
COINS_FILE = 'coins.json'

def fetch_all_coins():
    """
    Fetches a list of all active cryptocurrencies from the CoinMarketCap API.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }
    params = {
        "listing_status": "active",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin map from CoinMarketCap: {e}")
        return None

def save_coins_to_file(coins):
    """
    Saves the list of coins to a JSON file.
    """
    if coins is not None:
        with open(COINS_FILE, 'w') as f:
            json.dump(coins, f, indent=4)
        print(f"Successfully saved {len(coins)} coins to {COINS_FILE}")

def discover_coins():
    """
    Main function to fetch and save the list of coins.
    """
    print("Discovering coins...")
    coins = fetch_all_coins()
    if coins:
        save_coins_to_file(coins)

if __name__ == "__main__":
    discover_coins()
