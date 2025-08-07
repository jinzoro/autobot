import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
COINS_FILE = 'coins.json'

def fetch_cmc_coins():
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
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin map from CoinMarketCap: {e}")
        return []

def fetch_coingecko_coins():
    """
    Fetches a list of all cryptocurrencies from the CoinGecko API.
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coin list from CoinGecko: {e}")
        return []

def save_coins_to_file(coins):
    """
    Saves the list of coins to a JSON file.
    """
    if coins:
        with open(COINS_FILE, 'w') as f:
            json.dump(coins, f, indent=4)
        print(f"Successfully saved {len(coins)} coins to {COINS_FILE}")

def discover_coins():
    """
    Main function to fetch and save the list of coins from multiple sources.
    """
    print("Discovering coins...")
    cmc_coins = fetch_cmc_coins()
    cg_coins = fetch_coingecko_coins()

    # Merge the two lists, giving priority to CoinMarketCap data
    merged_coins = {coin['symbol'].upper(): coin for coin in cmc_coins}
    for coin in cg_coins:
        symbol = coin['symbol'].upper()
        if symbol not in merged_coins:
            merged_coins[symbol] = coin

    # Convert the dictionary back to a list
    final_coin_list = list(merged_coins.values())

    if final_coin_list:
        save_coins_to_file(final_coin_list)

if __name__ == "__main__":
    discover_coins()
