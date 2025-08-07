import discord
from discord.ext import commands
import json

COINS_FILE = 'coins.json'

@commands.command(name='search')
async def search(ctx, *, query: str):
    """
    Searches for a cryptocurrency by name or symbol.
    """
    try:
        with open(COINS_FILE, 'r') as f:
            coins = json.load(f)
    except FileNotFoundError:
        await ctx.send("The coin list is not available yet. Please try again in a few moments.")
        return

    query = query.lower()
    results = []
    for coin in coins:
        if query in coin['name'].lower() or query in coin['symbol'].lower():
            results.append(coin)

    if not results:
        await ctx.send(f"No coins found for '{query}'.")
        return

    embed = discord.Embed(
        title=f"Search Results for '{query}'",
        color=discord.Color.blue()
    )

    for coin in results[:10]:  # Limit to 10 results
        embed.add_field(
            name=f"{coin['name']} ({coin['symbol']})",
            value=f"Rank: {coin['rank']}",
            inline=False
        )

    if len(results) > 10:
        embed.set_footer(text=f"Showing 10 of {len(results)} results.")

    await ctx.send(embed=embed)
