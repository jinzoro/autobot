from discord.ext import tasks
import requests
import os

# Define the loop task
@tasks.loop(hours=1)
async def crypto_news(bot):
    channel_id = os.getenv("NEWS_CHANNEL_ID")
    if not channel_id:  # Check if channel_id is empty or None
        print("No NEWS_CHANNEL_ID set. Use !setnews to set the news channel.")
        return

    try:
        channel = bot.get_channel(int(channel_id))
    except ValueError:
        print("Invalid channel ID format. Please reset the news channel using !setnews.")
        return

    if channel is None:
        print("Invalid channel or bot doesn't have access. Please reset the news channel using !setnews.")
        return

    news_url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={os.getenv('NEWS_API_KEY')}"
    response = requests.get(news_url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        for article in articles[:5]:  # Send top 5 articles every hour
            await channel.send(f"{article['title']}\n{article['url']}")

# Function to start the loop task
def start_crypto_news(bot):
    crypto_news.start(bot)
