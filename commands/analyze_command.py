import discord
from discord.ext import commands
from utils.get_crypto_data import get_historical_data_binance, calculate_indicators
import datetime

@commands.command(name='analyze')
async def analyze(ctx, coin: str):
    intervals = ['1h', '4h', '1d']  # Intervals for analysis
    embed_description = ""
    overall_recommendation = ""
    recommendation_icon = ""
    thumbnail_url = ""  # URL for the icon to be shown in the top-left of the embed

    # Analyzing for each interval
    for interval in intervals:
        df = get_historical_data_binance(coin, interval=interval)
        if df is None:
            await ctx.send(f"Could not retrieve data for {coin}. Please check the coin symbol and try again.")
            return

        # Calculate indicators
        df = calculate_indicators(df)

        # Analyze indicators to determine long/short opportunities
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
        macd_diff = latest_macd - latest_macd_signal

        # Determine breakout analysis
        if latest_price > latest_ema_100 and latest_price > latest_ema_200:
            breakout_signal = "Bullish Breakout"
            recommendation = "📈 **Potential Long Opportunity**"
            if not overall_recommendation:
                overall_recommendation = "📈 Potential Long Opportunity"
                recommendation_icon = "📈"
                thumbnail_url = "https://your-icon-host.com/up-arrow.png"  # Replace with actual hosted URL
        elif latest_price < latest_ema_100 and latest_price < latest_ema_200:
            breakout_signal = "Bearish Breakout"
            recommendation = "📉 **Potential Short Opportunity**"
            if not overall_recommendation:
                overall_recommendation = "📉 Potential Short Opportunity"
                recommendation_icon = "📉"
                thumbnail_url = "https://your-icon-host.com/down-arrow.png"  # Replace with actual hosted URL
        else:
            breakout_signal = "No Breakout"
            recommendation = "⚖️ **No Clear Opportunity**"
            if not overall_recommendation:
                overall_recommendation = "⚖️ No Clear Opportunity"
                recommendation_icon = "⚖️"
                thumbnail_url = "https://your-icon-host.com/balance-scale.png"  # Replace with actual hosted URL

        # Analyze MACD for confirmation with threshold
        if macd_diff > 1:
            macd_signal = "MACD Bullish"
            if breakout_signal == "Bullish Breakout":
                recommendation = "🚀 **Strong Long Opportunity**"
                overall_recommendation = "🚀 Strong Long Opportunity"
                recommendation_icon = "🚀"
                thumbnail_url = "https://your-icon-host.com/rocket.png"  # Replace with actual hosted URL
        elif macd_diff < -1:
            macd_signal = "MACD Bearish"
            if breakout_signal == "Bearish Breakout":
                recommendation = "🔺 **Strong Short Opportunity**"
                overall_recommendation = "🔺 Strong Short Opportunity"
                recommendation_icon = "🔺"
                thumbnail_url = "https://your-icon-host.com/red-triangle.png"  # Replace with actual hosted URL
        else:
            macd_signal = "MACD Neutral"

        # RSI Analysis
        if latest_rsi < 30:
            rsi_signal = f"RSI is at {latest_rsi:.2f}, indicating **oversold** conditions (potential buy)."
        elif latest_rsi > 70:
            rsi_signal = f"RSI is at {latest_rsi:.2f}, indicating **overbought** conditions (potential sell)."
        else:
            rsi_signal = f"RSI is at {latest_rsi:.2f}, indicating a neutral range."

        # EMA Crossover Analysis
        if latest_ema_12 > latest_ema_26:
            ema_crossover_signal = "📈 **EMA 12/26 Bullish Crossover**: The short-term EMA (12) is above the long-term EMA (26), indicating an upward trend."
        elif latest_ema_12 < latest_ema_26:
            ema_crossover_signal = "📉 **EMA 12/26 Bearish Crossover**: The short-term EMA (12) is below the long-term EMA (26), indicating a downward trend."
        else:
            ema_crossover_signal = "⚖️ **EMA 12/26 Neutral**: No clear trend detected based on EMA crossover."

        # Long-term EMA Analysis
        if latest_ema_100 > latest_ema_200:
            ema_long_term_signal = "**Long-Term Uptrend**: The 100-day EMA is above the 200-day EMA, indicating a positive market outlook."
        else:
            ema_long_term_signal = "**Long-Term Downtrend**: The 100-day EMA is below the 200-day EMA, indicating a negative market outlook."

        # Append analysis for the current interval to the description
        embed_description += (
            f"**Interval: {interval}**\n"
            f"**Breakout Analysis**: {breakout_signal}\n"
            f"**EMA Crossover Analysis**: {ema_crossover_signal}\n"
            f"**Long-Term EMA Analysis**: {ema_long_term_signal}\n"
            f"**Recommendation**: {recommendation}\n"
            f"**MACD Analysis**: {macd_signal}\n"
            f"{rsi_signal}\n\n"
        )

    # Create and send embed message with analysis for all intervals
    embed = discord.Embed(
        title=f"{coin.upper()} Multi-Interval Analysis Report",
        description=f"{recommendation_icon} **Overall Recommendation**: {overall_recommendation}\n\n" + embed_description,
        color=discord.Color.purple()  # Set embed color to purple
    )
    embed.set_thumbnail(url=thumbnail_url)  # Set thumbnail image based on recommendation
    embed.set_footer(text=f"Analysis run at {datetime.datetime.utcnow()} UTC")
    await ctx.send(embed=embed)
