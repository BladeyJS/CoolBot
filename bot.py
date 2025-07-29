import discord
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

# --- AI Chat Response ---
async def get_ai_response(message_content):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are Coolbot, a helpful, chill AI assistant. You are cool and friendly."},
                {"role": "user", "content": message_content}
            ]
        }
        async with session.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except:
                return "Something went wrong. Try again later."

# --- Image Generation ---
async def generate_image(prompt):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "stability-ai/sdxl",
            "prompt": prompt,
        }
        async with session.post("https://api.together.xyz/v1/image/generation", headers=headers, json=payload) as resp:
            data = await resp.json()
            try:
                image_url = data["output"]["url"]
                return image_url
            except:
                return None

# --- On Ready ---
@client.event
async def on_ready():
    print(f"We are live as {client.user}!")

# --- On Message ---
@client.event
async def on_message(message):
    if message.author.bot:
        return

    bot_mentioned = client.user in message.mentions
    is_reply_to_bot = message.reference and message.reference.resolved and message.reference.resolved.author.id == client.user.id

    if bot_mentioned or is_reply_to_bot:
        clean_content = message.content.replace(f"<@{client.user.id}>", "").strip()

        if clean_content.lower().startswith("draw:"):
            prompt = clean_content[5:].strip()
            await message.channel.typing()
            image_url = await generate_image(prompt)
            if image_url:
                await message.channel.send(f"Here you go!\n{image_url}")
            else:
                await message.channel.send("Failed to generate image.")
        else:
            await message.channel.typing()
            response = await get_ai_response(clean_content)
            await message.channel.send(response)

client.run(DISCORD_TOKEN)

