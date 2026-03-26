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

_bot_data = None

def get_config() -> BotInfo:
    global _bot_data
    if _bot_data is None:
        _bot_data = load_bot_config()
    return _bot_data

class ConfigMeta(type):
    @property
    def bot_name(cls):
        return get_config().bot_name
    
    @property
    def data_id(cls):
        return get_config().data_id
    
    @property
    def owner(cls):
        return get_config().owner
    
    @property
    def command_prefix(cls):
        return get_config().command_prefix
    
    @property
    def colour(cls):
        bd = get_config()
        return discord.Colour.from_rgb(bd.colour[0], bd.colour[1], bd.colour[2])
    
    @property
    def listener_id(cls):
        if get_config().listener_id == None:
            return None
        return get_config().listener_id

class ConfigInfo(BotInfo, metaclass=ConfigMeta):
    pass


class AutoStatus():
    def __init__(self) -> None:
        self.list =[
            'LMAO',
            '67',
            'hello, world',
            'try /about',
            'I love slient...',
            'i\'m fine  ❤️‍🔥 ',
            'can you hear me?'
            ]

    def get_list(self):
        return self.list

class PureInfo():
    self_version = "0.0.1.a"
    update_time = "2025/03/21"
    latest_function = "/record"
    python_version = sys.version