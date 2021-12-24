import discord
import random
import re
import os
import requests
import youtube_dl
import asyncio
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands


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
            await channel.send("./play link")
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
