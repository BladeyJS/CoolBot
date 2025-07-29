import discord
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def generate_image(prompt):
    url = "https://api.together.xyz/v1/image/generate"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "stable-diffusion-v1",
        "prompt": prompt,
        "width": 512,
        "height": 512,
        "steps": 20
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            if resp.status != 200:
                print(f"Error generating image: {resp.status}")
                return None
            data = await resp.json()
            return data.get("url")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the bot is mentioned
    if client.user in message.mentions:
        content = message.content.replace(f"<@!{client.user.id}>", "").strip()
        if content.lower().startswith("image"):
            prompt = content[len("image"):].strip()
            if not prompt:
                await message.channel.send("Please provide a prompt after mentioning me and 'image'.")
                return
            await message.channel.send("Generating image, please wait...")
            image_url = await generate_image(prompt)
            if image_url:
                await message.channel.send(image_url)
            else:
                await message.channel.send("Failed to generate image.")
        else:
            # Just a normal text chat reply example (replace with your AI function)
            await message.channel.send(f"You said: {content}")

client.run(DISCORD_TOKEN)

bot.run(DISCORD_TOKEN)
