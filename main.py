import discord
from bot import Bot

intents = discord.Intents.default()
intents.voice_states = True

bot = Bot(intents=intents)
bot.run("ODI0ODg5Njc4ODkzMjg1Mzk2.G32C9H.18BKNWCRvOr-GWt-K6J0pygzpBL5KuwSlboWWE")
