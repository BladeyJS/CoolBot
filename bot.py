import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

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

@bot.event
async def on_ready():
    print(f"We are live as {bot.user}!")

@bot.command(name="coolbot")
async def coolbot_command(ctx, *, prompt: str):
    response = await get_ai_response(prompt)
    await ctx.send(response)

bot.run(DISCORD_TOKEN)

