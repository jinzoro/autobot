import discord
from discord.ext import commands
import os

@commands.command(name='setnews')
async def set_news_channel(ctx):
    news_channel_id = ctx.channel.id
    os.environ['NEWS_CHANNEL_ID'] = str(news_channel_id)
    with open('.env', 'a') as env_file:
        env_file.write(f'NEWS_CHANNEL_ID={news_channel_id}\n')
    await ctx.send(f"This channel has been set for crypto news updates.")
