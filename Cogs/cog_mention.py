import asyncio
import datetime
import discord

from discord import app_commands
from discord import Interaction
from discord.ext import commands
from typing import Optional

from tools.color import Color as C

class CogMention(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(
            name='bomb',
            callback=self.bomb, # set the callback of the context menu
        )
        self.client.tree.add_command(self.ctx_menu) # add the context menu to the app_commands


    async def bomb(self, interaction: Interaction, user: discord.Member):
        await interaction.response.send_message("compelete",ephemeral=True)
        channel = interaction.channel
        for _ in range(0,10):
            await channel.send(f'<@{user.id}>',delete_after=33.333)
            await asyncio.sleep(0.3)

    @app_commands.command(
        name="anon",
        description="send a message with Anonymous"
    )
    @app_commands.describe(
        channel_id = "channel's ID ,if not found or None will return current channel"
    )
    async def anon(self, interaction: Interaction, message: str, channel_id: Optional[str]):
        try:
            channel_id = int(channel_id)
        except:
            channel_id = 0
        if self.client.get_channel(int(channel_id)) == None:
            channel = interaction.channel
        else:
            channel = self.client.get_channel(int(channel_id))
        await interaction.response.send_message("compelepe!",ephemeral=True)
        msg = await channel.send(f'> ***Anonymous_user*** : {message}')
        dt = str(datetime.datetime.now())[:-7]
        print(f'{dt} {C.red}[Anonymous] -> (user : {interaction.user}, ID : {interaction.user.id}) | (message: {message} ,id: {msg.id}{C.reset})')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogMention(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_mention{C.reset}')