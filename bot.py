import discord
import os
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Function to call Together AI
async def get_ai_response(message):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are Coolbot, a helpful, chill AI assistant. You're also cool and friendly."},
                {"role": "user", "content": message}
            ]
        }
        async with session.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=json_data) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except:
                return "Oops, I couldn't think of anything to say."

# Event when bot is ready
@client.event
async def on_ready():
    print(f"We are live as {client.user}!")

# Event for message handling
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message starts with @Coolbot
    if message.content.startswith(client.user.mention):
        # Remove the bot mention from the message
        prompt = message.content.replace(client.user.mention, "").strip()

        if prompt:
            response = await get_ai_response(prompt)
            await message.channel.send(response)
        else:
            await message.channel.send("Hi! Mention me followed by your message so I can respond.")

# Run the bot
client.run(DISCORD_TOKEN)

