import datetime
import os
import sys

from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo

class CogSetups(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    #LOAD
    @commands.command()
    async def load(self, ctx:commands.Context, cog):
        if ctx.author.id == ConfigInfo.owner:
            try:
                await self.client.load_extension(f"Cogs.{cog.lower()}")
                await ctx.send(f"Successfully loaded **{cog}.py**") 
            except:
                await ctx.send(f"Error!")
        else:
            await ctx.send(f"No Permissions!")
    #RELOAD
    @commands.command()
    async def reload(self, ctx:commands.Context, cog):
        if ctx.author.id == ConfigInfo.owner:
            try:
                await self.client.reload_extension(f"Cogs.{cog.lower()}")
                await ctx.send(f"Successfully reloaded **{cog}.py**")
            except:
                await ctx.send(f"Error!")
        else:
            await ctx.send(f"No Permissions!")

    #Unload
    @commands.command()
    async def unload(self, ctx:commands.Context, cog):
        if ctx.author.id == ConfigInfo.owner:
            try:
                await self.client.unload_extension(f"Cogs.{cog.lower()}")
                await ctx.send(f"Successfully unloaded **{cog}.py**")
            except:
                await ctx.send(f"Error!")
        else:
            await ctx.send(f"No Permissions!")

    #ext_load(Extension_load)
    @commands.command()
    async def ext_load(self, ctx:commands.Context, extension):
        if ctx.author.id == ConfigInfo.owner:
            try:
                ext = os.listdir(f'./ext_{extension}')
                for i in ext:
                    if i == ('ext_loader.py'):
                        load = str(f'ext_{extension}.ext_loader')
                        await self.client.load_extension(load)
                        await ctx.send(f"Extension :{extension}.ext_loader")
            except:
                await ctx.send(f"Error!")
        else:
            await ctx.send(f"No Permissions!")

    #shut_down
    @commands.command()
    async def shut_down(self, ctx:commands.Context):
        if ctx.author.id == ConfigInfo.owner:
            await ctx.send(f"au revoir")
            await self.client.close()
            print(f'{C.purple}\t\t\t- - - - - - CLINET CLOSE - - - - - -{C.reset}')
        else:
            await ctx.send(f"No Permissions!")
            
    
    #re_start
    #if there are multiple bot data in `bot_data.ymal`
    #this command won't restart autocomplete
    @commands.command()
    async def re_start(self, ctx:commands.Context):
        if ctx.author.id == ConfigInfo.owner:
            dt = str(datetime.datetime.now())[:-7]
            await ctx.send(f"> {dt} Re_Start!")
            await self.client.close()
            print(f'{C.purple}\t\t\t- - - - - - CLINET CLOSE - - - - - -{C.reset}')
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await ctx.send(f"No Permissions!")


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogSetups(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_setup{C.reset}')