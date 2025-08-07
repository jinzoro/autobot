import discord
from discord.ext import commands
from utils.get_crypto_data import get_historical_data, calculate_indicators
import datetime

@commands.command(name='analyze')
async def analyze(ctx, coin: str):
    intervals = ['1h', '4h', '1d']  # Intervals for analysis
    embed_description = ""
    total_score = 0
    recommendation_icon = ""
    thumbnail_url = ""  # URL for the icon to be shown in the top-left of the embed

    for interval in intervals:
        df = get_historical_data(coin, interval=interval, limit='200')
        if df is None or df.empty:
            await ctx.send(f"Could not retrieve data for {coin} on interval {interval}. Please check the coin symbol and try again.")
            continue

        df = calculate_indicators(df)

        # --- Scoring System ---
        score = 0
        latest = df.iloc[-1]

        # RSI
        if latest['RSI'] < 30:
            score += 2
        elif latest['RSI'] > 70:
            score -= 2
        elif 30 <= latest['RSI'] < 50:
            score += 1
        elif 50 < latest['RSI'] <= 70:
            score -= 1

        # MACD
        if latest['MACD'] > latest['MACD_Signal']:
            score += 2
        else:
            score -= 2

        # EMA Crossover
        if latest['EMA_12'] > latest['EMA_26']:
            score += 2
        else:
            score -= 2

        # Long-Term Trend
        if latest['EMA_100'] > latest['EMA_200']:
            score += 1
        else:
            score -=1

        # Bollinger Bands
        if latest['close'] < latest['BB_Lower']:
            score += 2  # Oversold
        elif latest['close'] > latest['BB_Upper']:
            score -= 2  # Overbought

        # Stochastic Oscillator
        if latest['%K'] < 20 and latest['%D'] < 20 and latest['%K'] > latest['%D']:
            score += 2 # Bullish crossover in oversold territory
        elif latest['%K'] > 80 and latest['%D'] > 80 and latest['%K'] < latest['%D']:
            score -= 2 # Bearish crossover in overbought territory

        total_score += score

        # --- Generate Textual Analysis ---
        rsi_signal = f"RSI ({latest['RSI']:.2f})"
        macd_signal = "Bullish" if latest['MACD'] > latest['MACD_Signal'] else "Bearish"
        ema_signal = "Bullish" if latest['EMA_12'] > latest['EMA_26'] else "Bearish"
        bb_signal = "Neutral"
        if latest['close'] < latest['BB_Lower']:
            bb_signal = "Oversold"
        elif latest['close'] > latest['BB_Upper']:
            bb_signal = "Overbought"
        stoch_signal = f"%K: {latest['%K']:.2f}, %D: {latest['%D']:.2f}"


        embed_description += (
            f"**Interval: {interval} (Score: {score})**\n"
            f"- **RSI**: {rsi_signal}\n"
            f"- **MACD**: {macd_signal}\n"
            f"- **EMA Crossover**: {ema_signal}\n"
            f"- **Bollinger Bands**: {bb_signal}\n"
            f"- **Stochastic Osc.**: {stoch_signal}\n\n"
        )

    # --- Overall Recommendation ---
    if total_score >= 8:
        overall_recommendation = "🚀 **Strong Buy**"
        recommendation_icon = "🚀"
    elif 4 <= total_score < 8:
        overall_recommendation = "📈 **Buy**"
        recommendation_icon = "📈"
    elif -4 < total_score < 4:
        overall_recommendation = "⚖️ **Neutral**"
        recommendation_icon = "⚖️"
    elif -8 < total_score <= -4:
        overall_recommendation = "📉 **Sell**"
        recommendation_icon = "📉"
    else:
        overall_recommendation = "🔺 **Strong Sell**"
        recommendation_icon = "🔺"


    embed = discord.Embed(
        title=f"{coin.upper()} Comprehensive Analysis",
        description=f"**Overall Recommendation: {overall_recommendation} (Total Score: {total_score})**\n\n" + embed_description,
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"Analysis run at {datetime.datetime.utcnow()} UTC")
    await ctx.send(embed=embed)
