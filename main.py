import discord
import random
import os
from dotenv import load_dotenv
from discord.utils import get
from yt_dlp import YoutubeDL


class MyClient(discord.Client):

    @staticmethod
    async def join(textchannel, message):
        channel = message.author.voice.channel
        voice = get(client.voice_clients, guild=textchannel.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    @staticmethod
    async def add_to_queue(link, guildid):
        with YoutubeDL() as ydl:
            try:
                info = ydl.extract_info(link, download=False)
                trackTitle = info.get('title')
            finally:
                pass

        queueElement = {'link': link, 'title': trackTitle}
        if guildid in globalQueue:
            globalQueue.get(guildid).append(queueElement)
        else:
            globalQueue.update({guildid: [queueElement]})

    def play_from_queue(self, message):
        channel = client.get_channel(message.channel.id)
        if len(globalQueue.get(message.guild.id)) > 0:
            link = globalQueue.get(message.guild.id).pop(0).get('link')
            ydl_opts = {'format': 'bestaudio', 'outtmpl': 'track.%(ext)s'}

            if os.path.isfile("track.webm"):
                os.remove("track.webm")

            with YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([link])
                finally:
                    pass

            if channel:
                voice = get(client.voice_clients, guild=channel.guild)
                try:
                    source = discord.FFmpegPCMAudio("track.webm")
                    voice.play(source, after=lambda _: self.play_from_queue(message))
                    voice.source.volume = 1
                finally:
                    pass

    @staticmethod
    async def show_queue(message):
        channel = client.get_channel(message.channel.id)
        if not globalQueue.get(message.guild.id) is None:
            text_queue = '## Очередь:' + '\n'
            i = 0
            for track in globalQueue.get(message.guild.id):
                i += 1
                text_queue += '' + str(i) + '. [' + track.get('title') + '](<' + track.get('link') + '>)' + '\n'
        else:
            text_queue = 'Очередь пуста'
        await channel.send(text_queue)

    async def on_message(self, message):
        print(message.content)

        if message.content.startswith(f'{prefix}dice'):
            channel = client.get_channel(message.channel.id)
            try:
                await message.delete()
                author: str = message.author.name
                dies = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
                die1 = dies[random.randint(0, 5)]
                die2 = dies[random.randint(0, 5)]
                await channel.send(author + " бросает кости и выкидывает:   " + die1 + "   " + die2)
            except:
                await channel.send('err: Требуется выдать права на удаление сообщений')

        elif message.content.startswith(f'{prefix}p '):
            channel = client.get_channel(message.channel.id)
            await client.join(channel, message)
            templist = message.content.split()
            templist.pop(0)
            link = ''.join(templist)
            voice = get(client.voice_clients, guild=channel.guild)
            await self.add_to_queue(link, message.guild.id)
            if not voice.is_playing():
                try:
                    self.play_from_queue(message)
                finally:
                    pass

        elif message.content.startswith(f'{prefix}q'):
            await self.show_queue(message)

        elif message.content.startswith(f'{prefix}ch'):
            channel = client.get_channel(message.channel.id)
            voice = get(client.voice_clients, guild=channel.guild)
            if voice.is_playing():
                await channel.send("Играет баян")
            else:
                await channel.send("баян НЕ играет")
        elif message.content.startswith(f'{prefix}s'):
            channel = client.get_channel(message.channel.id)
            voice = get(client.voice_clients, guild=channel.guild)
            voice.stop()
            #self.play_from_queue(message)
            # await channel.send("Стоп")

        elif message.content.startswith(f'{prefix}pp'):
            channel = client.get_channel(message.channel.id)
            voice = get(client.voice_clients, guild=channel.guild)
            if voice and voice.is_paused():
                voice.resume()
            else:
                voice.pause()
        elif message.content.startswith(f'{prefix}h'):
            channel = client.get_channel(message.channel.id)
            await channel.send("История")


globalQueue = {}
load_dotenv()
token = os.getenv('TOKEN')

if os.getenv('TEST') == '1':
    prefix = '.'
else:
    prefix = '!'

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)
