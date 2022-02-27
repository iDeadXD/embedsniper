import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import moderator #cog moderator.py
import pytz

client = commands.Bot(command_prefix='prefix disini', intents=discord.Intents.all()) #prefix nya terserah

cogs = [moderator] #kalian bisa tambahin cogs yang sudah kalian buat (Harus di import terlebih dahulu)

for i in range(len(cogs)):
    cogs[i].setup(client) #Method setup yang ada di dalam Cogs

@client.event
async def on_ready():
    print('Bot Online')

client.run(os.environ.get('TOKEN'))
#client.run(os.getenv('TOKEN'))
