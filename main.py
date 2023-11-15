import discord
from bot import Bot

intents = discord.Intents.default()
intents.voice_states = True

bot = Bot(intents=intents)
bot.run("test")
