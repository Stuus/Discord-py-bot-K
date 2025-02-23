import asyncio
import datetime
import discord

from discord.ext import commands

from tools.set import ConfigInfo
from tools.set import AutoStatus


class CogStatus(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.auto_status_active = 0  #  0: stop auto_status
        self.stop_loop = 0           # -1: break the while loop


    #set_status
    @commands.command()
    async def set_status(self, ctx:commands.Context, status:str, game):
        if ctx.author.id == ConfigInfo.owner_id:
            self.auto_status_active = 0
            games = discord.Game(name=game)
            try:
                status = status.lower()
                if status.startswith('on'):
                    status = 'online'
                elif status.startswith('id'):
                    status = 'idle'
                elif status.startswith('dn'):
                    status = 'dnd'
                elif status.startswith('in'):
                    status = 'invisible'
                elif status.startswith('of'):
                    status = 'offline'
                self.stop_loop = -1
                msg = await ctx.send('pease wait')
                await asyncio.sleep(11)
                await self.client.change_presence(status=discord.Status(status), activity=games)
                content = (f'> change persence : status: {status}, activity: {game}.')
                await msg.edit(content=content)
                dt = str(datetime.datetime.now())[:-7]
                print(f'{dt} [Client] -> change persence : status: {status}, activity: {game}.')
            except:
                await ctx.send(f"ERROR!")
        else:
            await ctx.send(f"No Permissions!")

    #auto_status
    @commands.command()
    async def auto_status(self, ctx:commands.Context):
        if ctx.author.id == ConfigInfo.owner_id:
            await ctx.send(f'auto_status on!')
            self.auto_status_active = -1
        else:
            await ctx.send(f"No Permissions!")

        while self.auto_status_active == -1:
            status = 'dnd'
            auto_status = AutoStatus()
            for game in auto_status.get_list():
                if self.stop_loop == -1:
                    break
                games = discord.Game(name=game)
                await self.client.change_presence(status=discord.Status(status), activity=games)
                await asyncio.sleep(10)


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogStatus(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} [Cog] -> load cog_status')