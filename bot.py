import os
import discord
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# IMAGE GENERATION FUNCTION
async def generate_image(prompt):
    url = "https://api.together.xyz/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "stabilityai/stable-diffusion-2",  # You can change to other models if available
        "prompt": prompt,
        "width": 512,
        "height": 512,
        "steps": 30
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                try:
                    return result["data"][0]["url"]
                except:
                    return None
            else:
                print("Error status:", resp.status)
                return None

# COMMAND TO TRIGGER IMAGE GENERATION
@bot.command(name="image")
async def image(ctx, *, prompt: str):
    await ctx.send("🧠 Generating image, please wait...")
    image_url = await generate_image(prompt)
    if image_url:
        await ctx.send(f"🖼️ Here is your image for: **{prompt}**\n{image_url}")
    else:
        await ctx.send("❌ Failed to generate image. Try again later or check your prompt.")

# BOT READY
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# START
bot.run(DISCORD_TOKEN)
