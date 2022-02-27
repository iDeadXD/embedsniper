import discord
from discord.ext import commands
import asyncio
import pytz
from datetime import datetime
from pymongo import MongoClient
from config import CONFIG #config.py

dataclient = MongoClient(CONFIG['mongodb_url']) #Edit mongodb_url nya di config.py
database = dataclient['nama database'] #Sesuaikan dengan nama database yang kalian buat
saved = database['collection'] #Sesuaikan dengan nama collection pada saat kalian membuat database nya

class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener() #Event listener di dalam Cogs
    async def on_message_delete(self, message):
        data = saved.find_one({'_id': message.channel.id}) #Find document dari MongoDB dengan filter id channel saat ini 
        
        #Cek: Kalo message nya dalam bentuk embed
        if message.embeds:
            try:
                dev = self.client.get_user(#your id here) #Send message ke dev kalo embed yang terhapus (Optional)
                now = datetime.now(pytz.timezone('Asia/Jakarta')) #
                
                #Data embed yang bakal di ambil
                embed = message.embeds[0]
                embtitle = embed.title
                embdescription = embed.description
                embfooter = embed.footer.text
                embfootericon = embed.footer.icon_url
                embfields = embed.fields
                embimage = embed.image.url
                embthumbnail = embed.thumbnail.url
                
                #Kode yang berantakan
                title = 'None' if len(embtitle) == 0 else embtitle
                description = 'None' if len(embdescription) == 0 else embdescription
                footer = 'None' if len(embfooter) == 0 else embfooter
                footer_icon = 'None' if len(embfootericon) == 0 else embfootericon
                image = 'None' if len(embimage) == 0 else embimage
                fields = 'None' if len(embfields) == 0 else str(len(embfields))
                thumbnail = 'None' if len(embthumbnail) == 0 else embthumbnail
                
                #Cek: Kalo baru ada embed dihapus di channel saat ini atau sebaliknya
                if data is None:
                    new_data = {'_id': message.channel.id, 'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}', 'author': message.author.id}
                    saved.insert_one(new_data) #Membuat data baru dan memasukkannya ke databass
                    await dev.send(f'New Embed Data has been Saved!\nTimestamp: {now}\nServer: {message.guild.name}\nChannel: {message.channel.mention}\n-----------------------') #Send message ke Dev (Optional)
                else:
                    #Mengupdate data yang telah tersedia
                    saved.update_one({'_id': message.channel.id}, {'$set': {'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}', 'author': message.author.id}})
                    await dev.send(f'Embed Data has been Updated!\nTimestamp: {now}\nServer: {message.guild.name}\nChannel: {message.channel.mention}\n-----------------------') #Send message ke Dev (Optional)
            except Exception as e:
                return print(e)
    
    @commands.command(aliases=['se']) #Command di dalam Cogs
    async def snipe_embed(self, ctx):
        data = saved.find_one({'_id': ctx.channel.id}) #Find document dari MongoDB dengan filter id channel saat ini
        
        #Cek: Kalo ngga ada embed yang dihapus di channel saat ini
        if data is None:
            failed = discord.Embed(
                title='',
                description=f'No Embed was deleted last time on {ctx.channel.mention}',
                color=discord.Color.green()
            )
            return await ctx.send(embed=failed) #Bakal send error message
        
        author = self.client.get_user(data['author']) #Get user/author dari deleted embed
        recreate = discord.Embed(
            title='--- Embed Sniped! ---',
            description=f'Deleted Embed in {ctx.channel.mention}',
            color=discord.Color.purple(),
            timestamp=ctx.message.created_at
        )
        recreate.add_field(name='Title', value=f'{data["title"]}')
        recreate.add_field(name='Description', value=f'{data["description"]}')
        recreate.add_field(name='Footer', value=f'{data["footer"]}')
        recreate.add_field(name='Total Fields', value=f'{data["fields"]}')
        recreate.add_field(name='Footer Icon URL', value=f'{data["footer_icon"]}')
        recreate.add_field(name='Thumbnail URL', value=f'{data["thumbnail"]}')
        recreate.add_field(name='Image URL', value=f'{data["image"]}')
        recreate.add_field(name='Author', value=f'{author.name + "#" + author.discriminator} / {author.mention}')
        recreate.set_footer(text=f'Sniped by {ctx.author.name + "#" + ctx.author.discriminator}')
        
        await ctx.send(embed=recreate) #Send embed berisi data embed yang sebelumnya terhapus

#Setup
def setup(client):
    client.add_cog(Moderator(client))
