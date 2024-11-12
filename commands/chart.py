import discord
from discord.ext import commands
from utils.get_crypto_data import get_historical_data_binance_df
import datetime
import plotly.graph_objs as go
import plotly.io as pio
import os

@commands.command(name='chart')
async def chart(ctx, coin: str, interval: str = '1d', limit: str = '30'):
    # Get historical data from Binance
    historical_data = get_historical_data_binance_df(coin, interval, limit)

    if not historical_data:
        await ctx.send(f"Could not retrieve historical data for {coin}. Please check the coin symbol and try again.")
        return

    try:
        # Extract OHLC data for candlestick chart
        dates = [datetime.datetime.utcfromtimestamp(item["time"] / 1000) for item in historical_data]
        opens = [item["open"] for item in historical_data]
        highs = [item["high"] for item in historical_data]
        lows = [item["low"] for item in historical_data]
        closes = [item["close"] for item in historical_data]

        # Create the candlestick chart using Plotly
        candlestick = go.Candlestick(
            x=dates,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            increasing_line_color='green',  # Color for increasing candles
            decreasing_line_color='red',    # Color for decreasing candles
        )

        # Set up the figure
        layout = go.Layout(
            title=f'{coin.upper()} Price Chart - Interval: {interval}, Data Points: {limit}',
            xaxis_title='Date',
            yaxis_title='Price in USD',
            xaxis=dict(showgrid=True, rangeslider=dict(visible=False)),
            yaxis=dict(showgrid=True),
            template='plotly_dark',  # Dark theme
        )

        fig = go.Figure(data=[candlestick], layout=layout)

        # Save the chart as a static image
        file_name = f'{coin}_candlestick_chart.png'
        pio.write_image(fig, file_name)

        # Send the chart image in Discord
        with open(file_name, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

        # Clean up the file after sending
        os.remove(file_name)

    except KeyError:
        await ctx.send(f"Could not generate a chart for {coin}. Please try another cryptocurrency.")