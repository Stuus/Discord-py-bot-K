import datetime
import discord

from discord import app_commands
from discord.ext import commands

from tools.set import PureInfo

class CogInfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client



    #button
    class But(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        global message
        @discord.ui.button(label="close X",style=discord.ButtonStyle.red)
        async def t1(self,interaction:discord.Interaction,Button:discord.Button):
            await message.edit(content='==',delete_after=0.01)
            await interaction.response.send_message(".",delete_after=0.01)
        @discord.ui.button(label="Next ->",style=discord.ButtonStyle.green)
        async def t2(self,interaction:discord.Interaction,Button:discord.ui.Button):
            embed = discord.Embed(title=f" ",color=discord.Colour.from_rgb(218, 55, 60))
            embed.add_field(name=f"Update Time ",value=f'{PureInfo.update_time}')
            embed.add_field(name=f'Lastest Update',value=f'{PureInfo.lastest_function}')
            embed.add_field(name=f'Python Version',value=f'{PureInfo.python_verson}')
            await message.delete()
            await interaction.response.send_message(content="Page 2",embed=embed)

    #/about
    @app_commands.command(
        name="about",
        description="about this bot"
    )
    async def about(self, interaction:discord.Interaction):
        
        msg = (f"This is a discord bot Project By <@673156876095193088>.\n\
                `discord.py {discord.__version__}`\n\
                > ```diff\n\
                > +    _   __  _    _   _____     ___    ____   _    _    _     ___     \n\
                > +   | | / / | |  | | |  __ \   / _ \  / ___\ | |  | |  | |   / _ \    \n\
                > +   | |/ /  | |  | | | |__| | / / \ \  \ \   | |__| |  | |  / / \ \   \n\
                > +   |   |   | |  | | | __  / / /  / /   \ \  |  __  |  | | / /  / /   \n\
                > +   | |\ \  | \__/ / | | \ \ \ \_/ /  ___\ \ | |  | |  | | \ \_/ /    \n\
                > +   |_| \_\  \____/  |_|  \_\ \___/   \____/ |_|  |_|  |_|  \___/     \n\
                > +                                                                     \n\
                > -   async def on_message():                                           \n\
                > -   os.remove(\"main.py\")                                            \n\
                > ```")
        global message
        await interaction.response.send_message("==",delete_after=0.1)
        message = await interaction.channel.send(content=msg,view=CogInfo.But())

    #/get
    @app_commands.command(
        name= "get",
        description= "show sothing you want(#this function is Construct for developers)"
    )
    @app_commands.describe(object_you_want = "discord.Interaction")
    async def get(self,interaction: discord.Interaction,object_you_want : str):
        try:
            path = interaction
            for i in object_you_want.split("."):
                path = getattr(path , i)
            await interaction.response.send_message(f'> ```py\n> class Valume(discord.Interaction):\n>      discord.Interaction.{object_you_want}\n> \n> >>> {path}```')


        except AttributeError:
            await interaction.response.send_message(f'```py\nArithmeticError : discord.Interaction object has no attribute \'{object_you_want}\'\n```')





async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogInfo(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} [Cog] -> load cog_info')