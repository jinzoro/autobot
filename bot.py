import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from commands import crypto, setnews, chart, alert, predict, analyze_command, search
from tasks.crypto_news import start_crypto_news
from tasks.coin_analysis import analyze_coins
from tasks.discover_coins import discover_coins

# Load environment variables
load_dotenv()

# Setup intents
intents = discord.Intents.default()
intents.messages = True  # Enable access to messages
intents.guilds = True  # Enable access to guild information
intents.message_content = True  # Enable reading message content (needed for commands)

# Setup bot with command prefix and intents
bot = commands.Bot(command_prefix='!', description='AutoBot: Your crypto assistant', intents=intents)

# Load commands
bot.add_command(crypto.crypto)
bot.add_command(setnews.set_news_channel)
bot.add_command(chart.chart)
bot.add_command(alert.set_alert)
bot.add_command(predict.predict)
bot.add_command(analyze_command.analyze)
bot.add_command(search.search)



# Event listener for when the bot becomes ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # Discover all coins and save them to a file
    discover_coins()
    # Start the background tasks
    start_crypto_news(bot)
    analyze_coins.start()

# Store bot reference globally in analyze_coins
analyze_coins.bot = bot

# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
