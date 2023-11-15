import discord
import youtube_dl

class YouTube:
    def __init__(self):
        self.voice_client = None
        self.playlist = []
        self.is_playing = False

    async def play_song(self, message, query):
        voice_channel = message.author.voice.channel
        self.voice_client = await voice_channel.connect()

        if not self.is_playing:
            song_info = self.search_song(query)
            if song_info:
                self.playlist.append(song_info)
                await self.play_next_song()
            else:
                await message.channel.send("Sorry, I couldn't find the song.")

    async def play_next_song(self):
        if len(self.playlist) > 0:
            song_info = self.playlist[0]
            self.is_playing = True
            self.playlist = self.playlist[1:]

            voice_source = discord.FFmpegPCMAudio(song_info['url'])
            self.voice_client.play(voice_source, after=lambda e: self.play_next_song())

            await self.voice_client.channel.send(f"Now playing: {song_info['title']}")
        else:
            self.is_playing = False
            await self.voice_client.disconnect()

    async def skip_song(self, message):
        if self.is_playing:
            self.voice_client.stop()

    async def pause_song(self, message):
        if self.is_playing:
            self.voice_client.pause()

    async def resume_song(self, message):
        if self.is_playing:
            self.voice_client.resume()

    async def show_current_song(self, message):
        if self.is_playing:
            current_song = self.playlist[0]['title']
            await message.channel.send(f"Currently playing: {current_song}")
        else:
            await message.channel.send("No song is currently playing.")

    def search_song(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'},
            ],
            'noplaylist': True,
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                return {
                    'title': info['title'],
                    'url': info['url']
                }
            except Exception as e:
                print(f"An error occurred: {e}")