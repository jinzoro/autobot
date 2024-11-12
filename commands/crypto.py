import discord
from discord.ext import commands
from utils.get_crypto_data import get_crypto_data, get_crypto_metadata
import datetime

@commands.command(name='crypto')
async def crypto(ctx, coin: str):
    # Get crypto data for the provided coin symbol
    data = get_crypto_data(coin)
    metadata = get_crypto_metadata(coin)

    if not data or not metadata:
        await ctx.send(f"Could not retrieve data for {coin}. Please check the coin symbol and try again.")
        return

    try:
        # Extracting coin data
        coin_data = data['data'][coin.upper()]
        metadata_data = metadata['data'][coin.upper()]

        name = coin_data['name']
        quote = coin_data['quote']['USD']
        
        # Extracting financial data
        price = quote['price']
        volume_24h = quote['volume_24h']
        change_24h = quote['percent_change_24h']
        market_cap = quote['market_cap']
        ath = quote.get('ath', 'Not Available')
        high_24h = quote.get('high_24h', 'Not Available')
        low_24h = quote.get('low_24h', 'Not Available')

        circulating_supply = coin_data['circulating_supply']
        total_supply = coin_data.get('total_supply', 'Not Available')
        rank = coin_data['cmc_rank']
        logo = metadata_data.get('logo', '')  # Get the logo URL from metadata

        # Determine embed color and arrow icon based on price change
        if change_24h >= 0:
            color = 0x1abc9c  # Green for positive change
            arrow = "📈"  # Up arrow
        else:
            color = 0xff0000  # Red for negative change
            arrow = "📉"  # Down arrow

        # Create an embed message
        embed = discord.Embed(
            title=f"{name} (Rank #{rank})",
            color=color,
            timestamp=datetime.datetime.utcnow()  # Add a timestamp of the current time in UTC
        )

        # Add fields to embed (showing full precision)
        embed.add_field(name="Price", value=f"{arrow} ${price:,}", inline=True)
        embed.add_field(name="24h Change", value=f"{change_24h:.2f}%", inline=True)
        embed.add_field(name="24h High", value=f"${high_24h if high_24h != 'Not Available' else 'N/A'}", inline=True)
        embed.add_field(name="24h Low", value=f"${low_24h if low_24h != 'Not Available' else 'N/A'}", inline=True)
        embed.add_field(name="24h Volume", value=f"${volume_24h:,}", inline=True)
        embed.add_field(name="Market Cap", value=f"${market_cap:,}", inline=True)
        embed.add_field(name="All Time High", value=f"${ath if ath != 'Not Available' else 'N/A'}", inline=True)
        embed.add_field(name="Circulating Supply", value=f"{circulating_supply:,}", inline=True)
        embed.add_field(name="Total Supply", value=f"{total_supply if total_supply != 'Not Available' else 'N/A'}", inline=True)

        # Set thumbnail (if logo URL is available)
        if logo:
            embed.set_thumbnail(url=logo)

        # Add a footer for extra info
        embed.set_footer(text="Data provided by CoinMarketCap")

        # Send embed message
        await ctx.send(embed=embed)

    except KeyError:
        await ctx.send(f"Could not find complete data for {coin}. Please try another cryptocurrency.")
