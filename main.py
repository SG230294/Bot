import discord
import random
import re
import os
from dotenv import load_dotenv


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
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
        elif message.content.startswith(prefix + 'dice'):
            await message.delete()
            channel = client.get_channel(message.channel.id)
            author: str = message.author.name
            dies = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
            die1 = dies[random.randint(0, 5)]
            die2 = dies[random.randint(0, 5)]
            await channel.send(author + " бросает кости и выкидывает:   " + die1 + "   " + die2)
        elif message.content.startswith(prefix + 'rap'):
            channel = client.get_channel(message.channel.id)
            f = open('lyrics.txt', encoding="utf-8")
            lines = f.readlines()
            otvet = lines[random.randint(0, len(lines) - 1)]
            await channel.send(otvet)
        if message.content.startswith(prefix + 'test'):
            file = discord.File("Dice/1.jpg")
            await message.channel.send("", file=file)


load_dotenv()
client = MyClient()
client.run(os.getenv('TOKEN'))
