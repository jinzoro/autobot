import discord
from discord.ext import commands
import os
import json

# Store alerts in memory for now
alerts = []

@commands.command(name='alert')
async def set_alert(ctx, coin: str, target_price: str):
    # Remove commas and convert target_price to float
    try:
        target_price = float(target_price.replace(",", ""))
    except ValueError:
        await ctx.send("Invalid target price format. Please enter a valid number.")
        return

    # Create an alert
    alert = {
        "user_id": ctx.author.id,
        "channel_id": ctx.channel.id,
        "coin": coin.upper(),
        "target_price": target_price
    }
    alerts.append(alert)

    # Save alerts to a file (simple persistence)
    with open('alerts.json', 'w') as f:
        json.dump(alerts, f)

    # Confirmation message
    await ctx.send(f"Alert set for {coin.upper()} at ${target_price:.2f}. You will be notified once the price reaches your target.")

    # Private DM confirmation
    await ctx.author.send(f"Alert set for {coin.upper()} at ${target_price:.2f}. I will notify you when it hits the target.")
