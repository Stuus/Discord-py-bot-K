import discord
import sys
import time
import inputimeout

from . import yaml_tool
from .yaml_tool import BotInfo
from .color import Color

class LoginError(Exception):
    pass

def load_bot_config(*, current_data_id: int = -1) -> BotInfo:
    path = "./assets/bot_data.yaml"
    bot_objects = yaml_tool.load_bot_data(path=path)

    if bot_objects == []:
        raise LoginError(f"{Color.red}No Any bot data found. Please check path : `./assets/bot_data.yaml`{Color.reset}")

    if len(bot_objects) == 1:
        return bot_objects[0]

    elif len(bot_objects) > 1:
            print(f"{Color.blue}found multiple bot data(s)\nChoose one data to use:")
            for i in range(len(bot_objects)):
                bt = bot_objects[i]
                print(f"{Color.purple}{bt.bot_name:>5} : \t Enter [{i}]{Color.reset}")

            if current_data_id == -1:
                try:
                    c = int(inputimeout.inputimeout(prompt=f"{Color.yellow}Eneter number(if no input will start up [0]): {Color.reset}", timeout=15))
                except (inputimeout.TimeoutOccurred, ValueError):
                    c = 0

                if 0 <= c <= len(bot_objects):
                    current_data_id = c
                    return bot_objects[int(current_data_id)]
                else:
                    raise LoginError(f"{Color.red}Invalid number. Please try again.{Color.reset}")

            else:
                return bot_objects[current_data_id]

    else:
        raise LoginError(f"{bot_objects}")

bot_data = load_bot_config()

class ConfigInfo(BotInfo):
    bot_name = bot_data.bot_name
    data_id = bot_data.data_id
    owner = bot_data.owner
    command_prefix = bot_data.command_prefix
    colour = discord.Colour.from_rgb(bot_data.colour[0],bot_data.colour[1],bot_data.colour[2])
    listener_id = bot_data.listener_id


class AutoStatus():
    def __init__(self) -> None:
        self.list =[
            'hello, world',
            'try /about',
            'I love slient...',
            'i\'m fine  ❤️‍🔥 ',
            'can you hear me?'
            ]

    def get_list(self):
        return self.list

class PureInfo():
    self_vsrsion = "0.0.1.a"
    update_time = "2025/02/24"
    lastest_function = "N/A"
    python_verson = sys.version