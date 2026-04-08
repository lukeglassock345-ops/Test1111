import os
import random
import asyncio
import requests
import discord
from discord.ext import commands

# Load cookies from Railway variable
cookies_env = os.getenv("COOKIES", "")
cookies1 = cookies_env.split(",") if cookies_env else []

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.?', intents=intents)

@bot.event
async def on_ready():
    print("Bot is online!")

def follow_user(cookie, proxy, user_id):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie

            r = session.get("https://www.roblox.com/home")
            token = r.text.split("Roblox.XsrfToken.setToken('")[1].split("');")[0]
            session.headers['x-csrf-token'] = token

            session.post(
                f"https://friends.roblox.com/v1/users/{user_id}/follow",
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )
    except:
        pass

def add_user(cookie, user_id):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie

            r = session.get("https://www.roblox.com/home")
            token = r.text.split("Roblox.XsrfToken.setToken('")[1].split("');")[0]
            session.headers['x-csrf-token'] = token

            session.post(
                f"https://friends.roblox.com/v1/users/{user_id}/request-friendship",
                timeout=10
            )
    except:
        pass

@bot.command()
async def follow(ctx, user_id):
    await ctx.send(f"<@{ctx.author.id}>, follow bot started!")

    proxy_text = requests.get(
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=150000&country=all&ssl=all&anonymity=all"
    ).text

    proxies = proxy_text.splitlines()

    for cookie in cookies1:
        proxy = random.choice(proxies)
        await asyncio.to_thread(follow_user, cookie, proxy, user_id)
        await asyncio.sleep(0.01)

    await ctx.send("Finished sending follow requests!")

@bot.command()
async def friends(ctx, user_id):
    await ctx.send(f"<@{ctx.author.id}>, friend bot started!")

    for cookie in cookies1:
        await asyncio.to_thread(add_user, cookie, user_id)
        await asyncio.sleep(0.01)

    await ctx.send("Finished sending friend requests!")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

bot.run(TOKEN)
