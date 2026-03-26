import datetime
import discord

from discord import app_commands
from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo
from tools.set import PureInfo


class CogInfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client



    
    #/about
    page_one = (f"Page one\n\
                \n\
                This is a discord bot Project By <@673156876095193088>.\n\
                [View on Github](https://github.com/Stuus/Discord-py-bot-K)\n\
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

    @app_commands.command(
        name="about",
        description="about this bot"
    )
    async def about(self, interaction:discord.Interaction):
        await interaction.response.send_message(content=self.page_one, view=CogInfo.PageOne())

        #button_about
    class PageOne(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=120)

        @discord.ui.button(label="close x",style=discord.ButtonStyle.red)
        async def close_button(self,interaction:discord.Interaction,Button:discord.ui.Button):
            await interaction.message.delete()

        @discord.ui.button(label="Next ->",style=discord.ButtonStyle.green)
        async def next_button(self,interaction:discord.Interaction,Button:discord.ui.Button):
            embed = discord.Embed(title=f" ",color=ConfigInfo.colour)
            embed.add_field(name=f"Update Time ",value=f'{PureInfo.update_time}')
            embed.add_field(name=f'Lastest Update',value=f'{PureInfo.latest_function}')
            embed.add_field(name=f'Python Version',value=f'{PureInfo.python_version}')
            await interaction.response.edit_message(content="Page 2", embed=embed, view=CogInfo.PageTwo())
        
    class PageTwo(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=120)
            self.page_one = CogInfo.page_one

        @discord.ui.button(label="close x",style=discord.ButtonStyle.red)
        async def close_button(self,interaction:discord.Interaction,Button:discord.ui.Button):
            await interaction.message.delete()

        @discord.ui.button(label="Back <-",style=discord.ButtonStyle.green)
        async def back_button(self,interaction:discord.Interaction,Button:discord.ui.Button):
            await interaction.response.edit_message(content=self.page_one, view=CogInfo.PageOne(), embed=None)


    #/get
    #This command using getattr, malicious user could get sensitive information
    """
    @app_commands.command(
        name= "get",
        description= "show sothing you want(#Just play it, if you are developers)"
    )
    @app_commands.describe(object_you_want="discord.Interaction")
    async def get(self,interaction: discord.Interaction,object_you_want: str):
        warnings.warn(
            "This command using getattr, malicious user could get sensitive information",
            DeprecationWarning,
            stacklevel=2
        )
        try:
            path = interaction
            for i in object_you_want.split("."):
                path = getattr(path , i)
            
            result_message = f'> ```py\n> class Valume(discord.Interaction):\n>      discord.Interaction.{object_you_want}\n> \n> >>> {path}```'
            
            # anti leak token
            bot_token = interaction.client.http.token
            
            # if contains token
            if bot_token and bot_token in result_message:
                result_message = result_message.replace(bot_token, "<TOKEN has been blocked>")

            await interaction.response.send_message(result_message)

        except AttributeError:
            await interaction.response.send_message(f'```py\nArithmeticError : discord.Interaction object has no attribute \'{object_you_want}\'\n```')
    """




async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogInfo(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.lightblue}load cog_info{C.reset}')