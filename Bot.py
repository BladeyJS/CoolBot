import discord
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Function to call AI
async def get_ai_response(message):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": "meta-llama/Llama-3-8b-chat-hf",  # Choose another Together.ai model if you want
            "messages": [
                {"role": "system", "content": "You are Coolbot, a helpful, chill AI assistant. your also cool and friendly."},
                {"role": "user", "content": message}
            ]
        }
        async with session.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=json_data) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except:
                return "Oops, I couldn't think of anything to say."

@client.event
async def on_ready():
    print(f"We are live as {client.user}!")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!coolbot"):
        prompt = message.content[len("!coolbot "):]
        response = await get_ai_response(prompt)
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
