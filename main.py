import discord
import random
import re
import os
import requests
import asyncio
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands
from yt_dlp import YoutubeDL

globalQueue = {}


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
    def add_to_queue(link, guildid):
        if guildid in globalQueue:
            globalQueue.get(guildid).append(link)
        else:
            globalQueue.update({guildid: [link]})

    def play_from_queue(self, message):
        channel = client.get_channel(message.channel.id)
        if len(globalQueue.get(message.guild.id)) > 0:
            link = globalQueue.get(message.guild.id).pop(0)
            ydl_opts = {'format': 'bestaudio', 'outtmpl': 'track.%(ext)s', 'player_client' : 'tv_embedded'}

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
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("track.webm"))
                    voice.play(source, after=lambda _: self.play_from_queue(message))
                    voice.source.volume = 1
                finally:
                    pass

    async def on_message(self, message):
        print(message.content)
        if os.getenv('TEST') == '1':
            prefix = '.'
        else:
            prefix = '!'
        if message.content.startswith(f'{prefix}dice'):
            await message.delete()
            channel = client.get_channel(message.channel.id)
            author: str = message.author.name
            dies = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
            die1 = dies[random.randint(0, 5)]
            die2 = dies[random.randint(0, 5)]
            await channel.send(author + " бросает кости и выкидывает:   " + die1 + "   " + die2)
        elif message.content.startswith(f'{prefix}p'):
            channel = client.get_channel(message.channel.id)
            await client.join(channel, message)
            templist = message.content.split()
            templist.pop(0)
            link = ''.join(templist)

            voice = get(client.voice_clients, guild=channel.guild)
            if voice.is_playing():
                self.add_to_queue(link, message.guild.id)
            else:
                self.add_to_queue(link, message.guild.id)
                try:
                    self.play_from_queue(message)
                finally:
                    pass

        elif message.content.startswith(f'{prefix}rap') or re.search(r'рэп', message.content.lower()):
            # await message.delete()
            channel = client.get_channel(message.channel.id)
            f = open('lyrics.txt', encoding="utf-8")
            lines = f.readlines()
            otvet = lines[random.randint(0, len(lines) - 1)]
            await channel.send(otvet)
            text_to_speech = otvet
            apikey = '38da421963d847439fb86dcddff7cac3'
            language = 'ru-ru'
            request = requests.get(f'http://api.voicerss.org/?key={apikey}&src={text_to_speech}&hl={language}&v=Peter&f=8khz_8bit_stereo&r=1')
            with open('rap.mp3', 'wb') as file:
                file.write(request.content)
            if channel:
                await client.join(channel, message)
                voice = get(client.voice_clients, guild=channel.guild)
                voice.play(discord.FFmpegPCMAudio("rap.mp3"))
                voice.source.volume = 1
        elif message.content.startswith(f'{prefix}add'):
            channel = client.get_channel(message.channel.id)
            templist = message.content.split()
            templist.pop(0)
            link = ''.join(templist)
            self.add_to_queue(link, message.guild.id)
            print(globalQueue)
            await channel.send("добавленно в очередь")

        elif message.content.startswith(f'{prefix}q'):
            channel = client.get_channel(message.channel.id)
            if not globalQueue.get(message.guild.id) is None:
                text_queue = 'Очередь:' + '\n'
                i = 0
                for lnk in globalQueue.get(message.guild.id):
                    i += 1
                    text_queue += '['+str(i)+'] ['+lnk+']' + '\n'
            else:
                text_queue = 'Очередь пуста'
            await channel.send(text_queue)
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
            await channel.send("Стоп")
        if re.search(r'300[!?*.$%:;")( ]+$|300$|триста$|триста[!?*.$%:;")( ]+$', message.content.lower()):
            channel = client.get_channel(message.channel.id)
            if channel:
                await client.join(channel, message)
                voice = get(client.voice_clients, guild=channel.guild)
                voice.play(discord.FFmpegPCMAudio("otsosi.mp3"))
                voice.source.volume = 1


load_dotenv()
client = MyClient()
client.run(os.getenv('TOKEN'))
