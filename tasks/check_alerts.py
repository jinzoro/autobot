from discord.ext import tasks
import json
from utils.get_crypto_data import get_crypto_data
import discord

# Load alerts from file at startup
try:
    with open('alerts.json', 'r') as f:
        alerts = json.load(f)
except FileNotFoundError:
    alerts = []

@tasks.loop(minutes=1)  # Run this task every 1 minute
async def check_alerts(bot):
    # Iterate over alerts and check if the target price is reached
    for alert in alerts:
        coin_data = get_crypto_data(alert['coin'])
        if not coin_data:
            continue

        current_price = coin_data['data'][alert['coin']]['quote']['USD']['price']

        # Check if the price has reached the target
        if current_price == alert['target_price']:
            # Find user and channel
            user = await bot.fetch_user(alert['user_id'])
            channel = bot.get_channel(alert['channel_id'])

            # Create embed message
            embed = discord.Embed(title=f"{alert['coin']} Price Alert Triggered!", color=discord.Color.green())
            embed.add_field(name="Current Price", value=f"${current_price:.2f}", inline=False)
            embed.add_field(name="Target Price", value=f"${alert['target_price']:.2f}", inline=False)
            embed.set_footer(text="Price data provided by CoinMarketCap")
            
            # Send public channel alert
            if channel:
                await channel.send(embed=embed)

            # Send DM to the user
            if user:
                await user.send(embed=embed)

            # Remove the alert from the list since it has been triggered
            alerts.remove(alert)

            # Update the file after removal
            with open('alerts.json', 'w') as f:
                json.dump(alerts, f)
