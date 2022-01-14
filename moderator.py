import discord
from discord.ext import commands
import asyncio
import pytz
from datetime import datetime
from pymongo import MongoClient
from config import CONFIG

dataclient = MongoClient(CONFIG['mongodb_url'])
database = dataclient['database5']
saved = database['saved']

class Moderator(commands.Cog):
    """Moderator related commands. """
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        data = saved.find_one({'_id': message.guild.id})
        
        if message.embeds:
            try:
                dev = self.client.get_user(843132313562513408)
                now = datetime.now(pytz.timezone('Asia/Jakarta'))
                
                embed = message.embeds[0]
                embtitle = embed.title
                embdescription = embed.description
                embfooter = embed.footer.text
                embfootericon = embed.footer.icon_url
                embfields = embed.fields
                embimage = embed.image.url
                embthumbnail = embed.thumbnail.url
                
                #Identifier
                title = 'None' if len(embtitle) == 0 else embtitle
                description = 'None' if len(embdescription) == 0 else embdescription
                footer = 'None' if len(embfooter) == 0 else embfooter
                footer_icon = 'None' if len(embfootericon) == 0 else embfootericon
                image = 'None' if len(embimage) == 0 else embimage
                fields = 'None' if len(embfields) == 0 else str(len(embfields))
                thumbnail = 'None' if len(embthumbnail) == 0 else embthumbnail
                
                if data is None:
                    new_data = {'_id': message.guild.id, 'authorid': message.author.id, 'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}'}
                    saved.insert_one(new_data)
                    await dev.send(f'New Embed Data has been Saved!\nTimestamp: {now}\nChannel: {message.channel.mention}')
                else:
                    saved.update_one({'_id': message.guild.id}, {'$set': {'author_id': message.author.id, 'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}'}})
                    await dev.send(f'Embed Data has been Updated!\nTimestamp: {now}\nChannel: {message.channel.mention}')
            except Exception as e:
                return print(e)
    
    @commands.command(aliases=['se'])
    async def snipe_embed(self, ctx):
        data = saved.find_one({'_id': ctx.guild.id})
        
        if data is None:
            return
        
        recreate = discord.Embed(
            title='--- Embed Sniped! ---',
            description=f'**Title**: {data["title"]}',
            color=discord.Color.purple(),
            timestamp=ctx.message.created_at
        )
        recreate.add_field(name='Description', value=f'{data["description"]}')
        recreate.add_field(name='Footer', value=f'{data["footer"]}')
        recreate.add_field(name='Total Fields', value=f'{data["fields"]}')
        recreate.add_field(name='Footer Icon URL', value=f'{data["footer_icon"]}')
        recreate.add_field(name='Thumbnail URL', value=f'{data["thumbnail"]}')
        recreate.add_field(name='Image URL', value=f'{data["image"]}')
        recreate.set_footer(text=f'Sniped by {ctx.author.name + "#" + ctx.author.discriminator}')
        
        await ctx.send(embed=recreate)

def setup(client):
    client.add_cog(Moderator(client))
