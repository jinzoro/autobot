# AutoBot: Your Ultimate Crypto Companion

<p align="center">
  <a href="https://github.com/jinzoro/autobot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/jinzoro/autobot?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="License">
  </a>
  <a href="https://github.com/jinzoro/autobot/commits/main">
    <img src="https://img.shields.io/github/last-commit/jinzoro/autobot?style=for-the-badge&logo=git&logoColor=white&color=0080ff" alt="Last Commit">
  </a>
  <a href="https://github.com/jinzoro/autobot">
    <img src="https://img.shields.io/github/languages/top/jinzoro/autobot?style=for-the-badge&color=0080ff" alt="Top Language">
  </a>
  <a href="https://github.com/jinzoro/autobot">
    <img src="https://img.shields.io/github/languages/count/jinzoro/autobot?style=for-the-badge&color=0080ff" alt="Language Count">
  </a>
</p>

AutoBot is a feature-rich Discord bot designed to be your one-stop solution for all things crypto. Whether you're a seasoned trader or a curious beginner, AutoBot provides the tools and information you need to navigate the exciting world of cryptocurrencies.

## ✨ Features

AutoBot comes packed with a wide range of commands to help you stay ahead of the market:

| Command | Description | Example |
|---|---|---|
| `!crypto <coin>` | Get detailed price and market data for any cryptocurrency. | `!crypto BTC` |
| `!chart <coin> [interval] [limit]` | Generate a candlestick chart for a coin. | `!chart ETH 1h 50` |
| `!predict <coin> [interval]` | Get a price prediction and technical analysis. | `!predict SOL 4h` |
| `!analyze <coin>` | Perform a multi-interval technical analysis. | `!analyze ADA` |
| `!alert <coin> <target_price>` | Set a price alert for a coin. | `!alert DOGE 0.25` |
| `!setnews` | Set a channel for crypto news updates. | `!setnews` |

## 🚀 Getting Started

To get AutoBot up and running on your server, follow these simple steps:

### Prerequisites

- Python 3.8 or higher
- A Discord account and a server where you have administrative privileges.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jinzoro/autobot.git
    cd autobot
    ```

2.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** in the root directory and add your Discord bot token and CoinMarketCap API key:
    ```
    DISCORD_BOT_TOKEN=your_discord_bot_token
    COINMARKETCAP_API_KEY=your_coinmarketcap_api_key
    ```

4.  **Run the bot:**
    ```sh
    python bot.py
    ```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [CoinMarketCap API](https://coinmarketcap.com/api/)
- [Binance API](https://github.com/binance/binance-spot-api-docs)
- [Plotly](https://plotly.com/python/)
- [statsmodels](https://www.statsmodels.org/stable/index.html)
