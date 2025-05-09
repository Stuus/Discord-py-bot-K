import discord

from . import func
from .func import BotInfo
from .color import Color

class LoginError(Exception):
    pass

path = "./assets/bot_data.yaml"
bot_objects = func.load_bot_data(path=path)
current_data = 0

if bot_objects == []:
    raise LoginError(f"{Color.red}No Any bot data found. Please check path : `./assets/bot_data.yaml`{Color.reset}")

if len(bot_objects) == 1:
    bot_data:BotInfo = bot_objects[0]

elif len(bot_objects) > 1:    
        print(f"{Color.blue}found multiple bot data(s)\nChoose one data to use:")
        for i in range(len(bot_objects)):
            bt = bot_objects[i]
            print(f"{Color.purple}{bt.bot_name} : \t\t Enter [{i}]{Color.reset}")
        c = 0
        if current_data != 0:
            c = int(input('number: '))
            current_data = c
        bot_data:BotInfo = bot_objects[c]

else:
    raise LoginError(f"{bot_objects}")

class ConfigInfo():    
    owner = bot_data.owner
    command_prefix = bot_data.command_prefix
    colour = discord.Colour.from_rgb(bot_data.colour[0],bot_data.colour[1],bot_data.colour[2])
    token = bot_data.token
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
    update_time = "2025/02/24"
    lastest_function = "N/A"
    python_verson = "3.11.4"