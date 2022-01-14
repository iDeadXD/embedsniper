import os
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import moderation
import pytz

client = commands.Bot(command_prefix='**', intents=discord.Intents.all())

cogs = [moderation]

for i in range(len(cogs)):
    cogs[i].setup(client)

whitelist = [836464932236165140, 851745883825373225]

@client.event
async def on_ready():
    print('Bot Online')

@client.event
async def on_guild_join(guild):
    if guild.id not in whitelist:
        await guild.owner.send('Your Server Blacklisted!!')
        await guild.leave()

client.run(os.getenv('TOKEN'))
