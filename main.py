# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                   #
#   _   __  _    _   _____     ___    ____   _    _    _     ___    #
#  | | / / | |  | | |  __ \   / _ \  / ___\ | |  | |  | |   / _ \   #
#  | |/ /  | |  | | | |__| | / / \ \  \ \   | |__| |  | |  / / \ \  #
#  |   |   | |  | | | __  / / /  / /   \ \  |  __  |  | | / /  / /  #
#  | |\ \  | \__/ / | | \ \ \ \_/ /  ___\ \ | |  | |  | | \ \_/ /   #
#  |_| \_\  \____/  |_|  \_\ \___/   \____/ |_|  |_|  |_|  \___/    #
#                                                                   #
#                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 
import asyncio
import datetime
import discord
import os
import random
import sys
import typing
import yaml


from discord.ext import commands

from tools.set import ConfigInfo
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class CogRead:
    cogs = []
    try:
        # If the file package to `.exe` , than sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    cogs_path = os.path.join(base_path, "Cogs")

    if os.path.exists(cogs_path):
        for Filename in os.listdir(cogs_path):
            if Filename.startswith('cog'):
                add = str(f'Cogs.{Filename[:-3]}')
                cogs.append(add)
    else:
        print(f"Error: Cogs folder not found at {cogs_path}")

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='bot: ', intents=discord.Intents().all())
        self.cogslist = CogRead.cogs

    async def on_ready(self):
        dt = str(datetime.datetime.now())[:-7]
        print(f'{dt} Logged with :  {self.user.name}')
        synced = await self.tree.sync()
        command_names = [command.name for command in synced]
        print(f'                    Application commands Synced  {str(len(synced))}   Commands')
        print(f'                    {command_names}')

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

client = Client()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

client.run(ConfigInfo.token)