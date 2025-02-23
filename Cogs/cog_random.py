import discord
import datetime
import random

from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from typing import Optional

from tools.color import Color as C
from tools.func import xfill
from tools.set import ConfigInfo

class CogRandom(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    class Tmp():
        option = []

    class RandomModal(discord.ui.Modal, title = "又選不出來了?"):
        opt : discord.ui.TextInput = discord.ui.TextInput(label="增加選項",placeholder="打甚麼都可以")
        async def on_submit(self, interaction: discord.Interaction):
            CogRandom.Tmp.option.append(str(self.opt.value))
            content = f'已增加選項: `{self.opt.value}`'
            await interaction.response.send_message(content=content,delete_after=120)

    @app_commands.command(
        name = "random",
        description = "抽一個大的"
    )
    @app_commands.choices(mode=[
        Choice(name='增加選項', value=1),
        Choice(name='開始',  value=2)
    ])
    @app_commands.describe(reason="你要選什麼?")
    async def random(
        self,
        interaction : discord.Interaction,
        mode : Choice[int],
        reason : Optional[str]
    ):
        if mode.value == 1: #add choice mode
            await interaction.response.send_modal(self.RandomModal())
        elif mode.value == 2: #start mode
            if self.Tmp.option == []:
                await interaction.response.send_message(content="還沒有選項!",ephemeral=True)
            else:
                if reason == None:
                    reason = " "
                embed = discord.Embed(title=f"{reason} 結果出爐!",color=ConfigInfo.colour)
                ran = [random.randint(1,99) for _ in range(len(self.Tmp.option))]

                for i in range(len(self.Tmp.option)):
                    self.Tmp.option[i] = [ran[i],self.Tmp.option[i]]
                self.Tmp.option.sort()

                for i in range(len(self.Tmp.option)):
                    number = 100 - int(self.Tmp.option[i][0])
                    view = xfill(num=int(number),length=40)
                    v = f'```ini\n{view}\n{number}%\n```'
                    embed.add_field(name=self.Tmp.option[i][1],value=v,inline=False)
                    
                await interaction.response.send_message("GG",delete_after=0.1)
                await interaction.channel.send(embed=embed)
                self.Tmp.option = []


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogRandom(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_random{C.reset}')