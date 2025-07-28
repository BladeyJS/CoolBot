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

async def get_ai_response(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": "You are Coolbot, a friendly, chill assistant with a cool personality."},
            {"role": "user", "content": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            response = await resp.json()
            try:
                return response["choices"][0]["message"]["content"]
            except:
                return "Something went wrong with the AI response."

@client.event
async def on_ready():
    print(f"✅ Coolbot is online as {client.user}!")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    mentioned = client.user in message.mentions
    is_reply = (
        message.reference and
        isinstance(message.reference.resolved, discord.Message) and
        message.reference.resolved.author == client.user
    )

    if mentioned or is_reply:
        # Remove bot mention from prompt (if mentioned)
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not prompt:
            prompt = message.content.strip()

        response = await get_ai_response(prompt)
        await message.channel.send(response)

client.run(DISCORD_TOKEN)

