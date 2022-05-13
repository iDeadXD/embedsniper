import os
import discord #pip install discord.py (pakai discord.py 1.7.3)
from discord.ext import commands
import asyncio
from datetime import datetime
import embed #Cog embed.py
import pytz

client = commands.Bot(command_prefix='prefix disini', intents=discord.Intents.default()) #prefix nya terserah

cogs = [embed] #kalian bisa tambahin cogs yang sudah kalian buat (Harus di import terlebih dahulu)

for i in range(len(cogs)):
    cogs[i].setup(client) #Method setup yang ada di dalam Cogs

@client.event
async def on_ready():
    print('Bot Online')

client.run('TOKEN')
#client.run(os.getenv('TOKEN'))
#client.run('Langsung Token')
