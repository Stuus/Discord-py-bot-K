import discord
import datetime
import random

from discord import app_commands
from discord.ext import commands
from typing import Optional

from tools.color import Color as C
from tools.func import yaml_loader,YamlLoaderError
from tools.set import ConfigInfo


class CogWeapons(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client
        try:
            self.weapons = yaml_loader(path='./assets/choice_zh.yaml') # TODO(Stuus) : Need a switch to change local Languages
        except YamlLoaderError as e:
            print(f"Error loading weapons: {e}")
            self.weapons = {}

    @app_commands.command(
        name="lucky_weapon",
        description="Lucky Weapon!"
    )
    async def lucky_weapon(self, interaction:discord.Interaction):
        user_id = (f'<@{interaction.user.id}>')

        weapon = random.sample(self.weapons['ValorantWeapons'],2)
        embed = discord.Embed(title=f"結果出爐!",color=ConfigInfo.colour)
        embed.set_author(name=interaction.user,
                         icon_url=interaction.user.display_avatar
                         )
        embed.add_field(name="__你現在的幸運武器是__",value=weapon[0],inline=True)
        embed.add_field(name="   |",value="   |",inline=True)
        embed.add_field(name="__最好別用__",value=weapon[1],inline=True)
        await interaction.response.send_message(content=user_id,embed=embed)
        


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogWeapons(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_weapons{C.reset}')