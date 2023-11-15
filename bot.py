import discord
from youtube import YouTube

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.youtube = YouTube()

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!play'):
            query = message.content[6:].strip()
            await self.youtube.play_song(message, query)
        
        elif message.content == '!skip':
            await self.youtube.skip_song(message)
        
        elif message.content == '!pause':
            await self.youtube.pause_song(message)
        
        elif message.content == '!resume':
            await self.youtube.resume_song(message)
        
        elif message.content == '!current':
            await self.youtube.show_current_song(message)