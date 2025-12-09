import datetime
import discord

from discord import app_commands
from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo



class CogVoiceClient(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client
    
    @app_commands.command(
        name = "join",
        description = "Make the bot join your voice channel"
    )
    async def join(self, interaction:discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel.",ephemeral=True,delete_after=60)
            return
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"Joined {channel}.")


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogVoiceClient(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_voice_client{C.reset}')