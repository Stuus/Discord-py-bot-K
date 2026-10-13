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
        channel = interaction.channel
        if isinstance(channel, discord.abc.Messageable):
            for _ in range(0,10):
                await channel.send(f'<@{user.id}>',delete_after=33.333)
                await asyncio.sleep(0.3)
                await interaction.response.send_message("complete",ephemeral=True)
        else:
            await interaction.response.send_message("This channel is not messageable.", ephemeral=True)
            

    @app_commands.command(
        name="anon",
        description="send a message with Anonymous"
    )
    @app_commands.describe(
        channel_id = "channel's ID ,if not found or None will return current channel"
    )
    async def anon(self, interaction: Interaction, message: str, channel_id: Optional[int]):
        
        _get_channel = self.client.get_channel(channel_id) if channel_id is not None else interaction.channel

        if _get_channel is None:
            await interaction.response.send_message("Channel not found.", ephemeral=True)
            return
        elif not isinstance(_get_channel, discord.abc.Messageable):
            await interaction.response.send_message("Designated channel is not messageable.", ephemeral=True)
            return
        
        await interaction.response.send_message("complete", ephemeral=True)
        msg = await _get_channel.send(f'> ***Anonymous_user*** : {message}')
        dt = str(datetime.datetime.now())[:-7]
        print(f'{dt} {C.red}[Anonymous] -> (user : {interaction.user}, ID : {interaction.user.id}) | (message: {message} ,id: {msg.id}{C.reset})')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogMention(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.lightblue}load cog_mention{C.reset}')