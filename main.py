import discord
import random
import re
import os
import youtube_dl
import requests
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from discord.utils import get
import pyglet

class MyClient(discord.Client):

    async def join(self, textchannel, message):
        channel = message.author.voice.channel
        voice = get(client.voice_clients, guild=textchannel.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print(message.content)
        if os.getenv('TEST') == '1':
            prefix = '.'
        else:
            prefix = '!'
        if re.search(r'нигер', message.content.lower()):
            osuzhdenie = ':man_gesturing_no_tone5: Осуждаю! :man_gesturing_no_tone5:'
            if re.search(r'пидор', message.content.lower()):
                osuzhdenie = ':rainbow_flag: СУПЕР ОСУЖДЕНИЕ! :man_gesturing_no_tone5:'
            await message.reply(osuzhdenie, mention_author=True)
        elif re.search(r'пидор', message.content.lower()):
            await message.reply(':rainbow_flag: Осуждаю! :rainbow_flag:', mention_author=True)
        elif message.author.id == self.user.id:
            return
        elif message.content.startswith(f'{prefix}dice'):
            # await message.delete()
            channel = client.get_channel(message.channel.id)
            author: str = message.author.name
            dies = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
            die1 = dies[random.randint(0, 5)]
            die2 = dies[random.randint(0, 5)]
            await channel.send(author + " бросает кости и выкидывает:   " + die1 + "   " + die2)
        elif message.content.startswith(f'{prefix}rap') or re.search(r'рэп', message.content.lower()):
            # await message.delete()
            channel = client.get_channel(message.channel.id)
            f = open('lyrics.txt', encoding="utf-8")
            lines = f.readlines()
            otvet = lines[random.randint(0, len(lines) - 1)]
            await channel.send(otvet)
            text_to_speech = otvet
            request = requests.get(f'http://api.voicerss.org/?key=38da421963d847439fb86dcddff7cac3&src={text_to_speech}&hl=ru-ru&v=Peter&f=8khz_8bit_stereo')
            with open('rap.mp3', 'wb') as file:
                file.write(request.content)
            if channel:
                await client.join(channel, message)
                voice = get(client.voice_clients, guild=channel.guild)
                voice.play(discord.FFmpegPCMAudio("rap.mp3"))
                voice.source.volume = 1

        elif message.content.startswith(f'{prefix}beat'):
             channel = client.get_channel(message.channel.id)
            # await client.join(channel, message)
            # song_there = os.path.isfile("song.mp3")
            # try:
            #     if song_there:
            #         os.remove("song.mp3")
            #         print("Removed old song file")
            # except PermissionError:
            #     print("Trying to delete song file, but it's being played")
            #     await channel.send("ERROR: Music playing")
            #     return
            #
            # voice = get(client.voice_clients, guild=channel.guild)
            #
            # ydl_opts = {
            #     'format': 'bestaudio/best',
            #     'postprocessors': [{
            #         'key': 'FFmpegExtractAudio',
            #         'preferredcodec': 'mp3',
            #         'preferredquality': '192',
            #     }],
            # }
            #
            # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #     print("Downloading audio now\n")
            #     ydl.download(['https://youtu.be/zxASJ0X3784'])
            # for file in os.listdir("./"):
            #     if file.endswith(".mp3"):
            #         print(f"Renamed File: {file}\n")
            #         os.rename(file, "song.mp3")
            # voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
            # voice.source = discord.PCMVolumeTransformer(voice.source)
            # voice.source.volume = 1


load_dotenv()
client = MyClient()
client.run(os.getenv('TOKEN'))
