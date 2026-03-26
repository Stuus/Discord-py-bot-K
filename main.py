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
import dotenv
import os
import random
import sys
import traceback
import typing
import yaml

from discord.ext import commands
from dotenv import load_dotenv

from tools.color import Color as C
from tools.set import ConfigInfo, PureInfo





# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class CogRead:
    @classmethod
    def get_cogs(cls):
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
            print(f"{C.red}Error: Cogs folder not found at {cogs_path}{C.reset}")
        return cogs

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class Client(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(
            intents=discord.Intents().all(),
            **kwargs
            )
        self.cogslist = CogRead.get_cogs()

    async def on_ready(self):
        dt = str(datetime.datetime.now())[:-7]
        print(f'                    {C.lightblue}Bot Version: {PureInfo.self_version}{C.reset}')
        # TODO: 檢查 github 上的最新發布，如果有新版本則 DM bot_owner
        
        # get shard info of this process
        shards_info = list(self.shards.keys()) if self.shards else "Auto"
        print(f'{dt}{C.green} Logged with :  {self.user.name}{C.reset} Shards : {shards_info} (Total: {self.shard_count}){C.reset}')
        synced = await self.tree.sync()
        command_names = [command.name for command in synced]
        print(f'{C.blue}                    Application commands Synced  {str(len(synced))}   Commands')
        print(f'                    {command_names}{C.reset}')

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if __name__ == "__main__":
    try:
        load_dotenv()
        env_token = os.getenv(f"{ConfigInfo.bot_name}_TOKEN")
        
        shard_kwargs = {}
        # If .env file has SHARD_ID, it will enable manual sharding and lock a single Shard
        if os.getenv("SHARD_ID") is not None:
            shard_kwargs['shard_ids'] = [int(os.getenv("SHARD_ID"))]
            # Read the total number of shards (default to 3 to prevent errors)
            shard_kwargs['shard_count'] = int(os.getenv("SHARD_COUNT", "3"))

        # if kwargs is empty, AutoShardedBot will automatically start and take over all shards
        client = Client(command_prefix=ConfigInfo.command_prefix,**shard_kwargs)

        client.run(token= env_token)
    except Exception as e:
        print(f"{C.red}Error while running bot process: {e}{C.reset}")
        traceback.print_exc()
    finally:
        dt = str(datetime.datetime.now())[:-7]
        print(f'{dt} {C.yellow}Bot Shutdown.{C.reset}')
        sys.exit(0)