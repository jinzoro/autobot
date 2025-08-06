import discord
from discord.ext import commands
from utils.get_crypto_data import get_historical_data_binance, calculate_indicators, arima_forecast, generate_forecast_chart
import pandas as pd

@commands.command(name='predict')
async def predict(ctx, coin: str, interval: str = '1d'):
    # Validate interval
    valid_intervals = ['1h', '4h', '12h', '1d']
    if interval not in valid_intervals:
        await ctx.send(f"Invalid interval. Please use one of the following: {', '.join(valid_intervals)}.")
        return

    # Get historical data for the specified coin and interval
    df = get_historical_data_binance(coin, interval, limit='200') # Increased limit for better forecasting
    if df is None:
        await ctx.send(f"Could not retrieve historical data for {coin}. Please check the coin symbol.")
        return

    # Calculate indicators
    df = calculate_indicators(df)

    # Analyze EMAs to make a prediction
    latest_price = df['close'].iloc[-1]
    latest_ema_12 = df['EMA_12'].iloc[-1]
    latest_ema_26 = df['EMA_26'].iloc[-1]
    latest_ema_100 = df['EMA_100'].iloc[-1]
    latest_ema_200 = df['EMA_200'].iloc[-1]
    latest_rsi = df['RSI'].iloc[-1]

    # Calculate MACD and MACD Signal Line
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    latest_macd = df['MACD'].iloc[-1]
    latest_macd_signal = df['MACD_Signal'].iloc[-1]

    # Determine buy or sell signal based on EMA 12 and EMA 26
    if latest_ema_12 > latest_ema_26:
        signal = "📈 **Buy Signal**: The short-term EMA is above the long-term EMA, indicating an upward trend."
    elif latest_ema_12 < latest_ema_26:
        signal = "📉 **Sell Signal**: The short-term EMA is below the long-term EMA, indicating a downward trend."
    else:
        signal = "⚖️ **Neutral**: No clear trend detected based on EMA crossovers."

    # Analyze EMA 100 and EMA 200 for long-term trend
    if latest_ema_100 > latest_ema_200:
        long_term_trend = "**Long-Term Uptrend**: The 100-day EMA is above the 200-day EMA, indicating a positive market outlook."
    else:
        long_term_trend = "**Long-Term Downtrend**: The 100-day EMA is below the 200-day EMA, indicating a negative market outlook."

    # MACD Analysis
    if latest_macd > latest_macd_signal:
        macd_signal = "📊 **MACD Bullish**: The MACD line is above the Signal line, indicating a potential uptrend."
    elif latest_macd < latest_macd_signal:
        macd_signal = "📊 **MACD Bearish**: The MACD line is below the Signal line, indicating a potential downtrend."
    else:
        macd_signal = "📊 **MACD Neutral**: No clear trend detected based on MACD."

    # Breakout Analysis
    if latest_price > latest_ema_100 and latest_price > latest_ema_200:
        breakout_signal = "🚀 **Bullish Breakout**: The price has broken above both EMA 100 and EMA 200, indicating strong upward momentum."
    elif latest_price < latest_ema_100 and latest_price < latest_ema_200:
        breakout_signal = "📉 **Bearish Breakout**: The price has fallen below both EMA 100 and EMA 200, indicating strong downward momentum."
    else:
        breakout_signal = "⚖️ **No Breakout**: The price is between EMA 100 and EMA 200, indicating no clear breakout."

    # Add RSI information
    if latest_rsi < 30:
        rsi_signal = f"RSI is at {latest_rsi:.2f}, which indicates **oversold** conditions (potential buy opportunity)."
    elif latest_rsi > 70:
        rsi_signal = f"RSI is at {latest_rsi:.2f}, which indicates **overbought** conditions (potential sell opportunity)."
    else:
        rsi_signal = f"RSI is at {latest_rsi:.2f}, which is in the normal range."

    # Perform ARIMA forecast
    forecast, error_message = arima_forecast(df, forecast_periods=5)
    if error_message:
        forecast_text = f"**ARIMA Forecast**: {error_message}"
    else:
        forecast_text = "**ARIMA Forecast (next 5 periods)**:\n"
        for i, val in enumerate(forecast):
            forecast_text += f"Period {i+1}: {val:.4f}\n"

    # Create and send embed message with prediction
    embed = discord.Embed(
        title=f"{coin.upper()} Price Prediction & Analysis ({interval} Interval)",
        description=f"{signal}\n\n{long_term_trend}\n\n{macd_signal}\n\n{breakout_signal}\n\n{rsi_signal}\n\n{forecast_text}",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Technical analysis and forecasts are not financial advice. Trade responsibly.")

    # Generate and attach chart if forecast is available
    if forecast is not None:
        chart_buf = generate_forecast_chart(df, forecast, coin, interval)
        file = discord.File(chart_buf, filename=f"{coin.lower()}_forecast.png")
        embed.set_image(url=f"attachment://{coin.lower()}_forecast.png")
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(embed=embed)
