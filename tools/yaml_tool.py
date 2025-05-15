import yaml
import sys
import os

from typing import Dict, List, Optional
from .color import Color as C

#.yaml to class
class BotInfo:
    def __init__(self, bot_name, owner, command_prefix, colour, token, listener_id):
        self.bot_name = bot_name
        self.owner = owner
        self.command_prefix = command_prefix
        self.colour = colour
        self.token = token
        self.listener_id = listener_id

    def __repr__(self):
        return (f"BotInfo(bot_name='{self.bot_name}', owner={self.owner}, "
                f"command_prefix='{self.command_prefix}', colour={self.colour}, "
                f"token='{self.token}', listener_id={self.listener_id})")

def bot_info_constructor(loader, node):
    values = loader.construct_mapping(node)
    return BotInfo(**values)

def load_bot_data(path,*,pass_none : bool | None = True):
    yaml.add_constructor("!BotInfo", bot_info_constructor, yaml.SafeLoader)
    yaml.add_constructor("!BotInfoExample", bot_info_constructor, yaml.SafeLoader)

    try:
        if hasattr(sys, '_MEIPASS'):  # Check if running in PyInstaller
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        full_path = os.path.join(base_path, path)

        with open(full_path, 'r') as file:
            data = yaml.safe_load(file)

        bot_instances = []
        for item in data:
            if isinstance(item, BotInfo):
                if pass_none == True and (item.bot_name == "example" or item.bot_name is None):
                    continue
                bot_instances.append(item)

        return bot_instances
    
    except FileNotFoundError:
        raise YamlLoaderError(f"yaml_loader error : file path'{path}' not found.")

    except yaml.YAMLError as e:
        raise YamlLoaderError(f"yaml_loader error : {e}")

#yaml_loader
class YamlLoaderError(Exception):
    pass

def yaml_loader(path : str, * , mode : str | None = "r", encode : str | None = "utf-8") -> Dict[str, List]:
    """
    Read yaml file and return a dict

    Args:
        path        (str) : file path.
        pass_none   (bool): if true, ignore data that bot_name is None.
        mode        (str) : open() open text mode.
        encode      (str) : encoding.

    Returns:
        dict[str,list]

    Raises:
        YamlLoaderError: if file not found or yaml parse failed.

    """
    try:
        if hasattr(sys, '_MEIPASS'):  # Check if running in PyInstaller
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        full_path = os.path.join(base_path, path)

        with open(full_path, mode=mode, encoding=encode) as file:
            print(f"{C.green}yaml_loader opened({mode}): {C.yellow}'{full_path}'{C.reset}")
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        raise YamlLoaderError(f"yaml_loader error : file path'{path}' not found.")

    except yaml.YAMLError as e:
        raise YamlLoaderError(f"yaml_loader error : {e}")

#update_bot_info #TODO(stuus) : ..
def update_bot_info(path:str, bot_name, new_data:dict):
    """
    replace YAML From `bot_name`.

    Args:
    path       : file path.
    bot_name   : item `bot_name`.
    new_data   : dict.
    """
    try:
        data = yaml_loader(path)
    except YamlLoaderError as e:
        print(e)
        return

    # find the item with the specified bot_name
    updated = False
    for item in data:
        if isinstance(item, dict) and item.get('!BotInfo', {}).get('bot_name') == bot_name:
            item['!BotInfo'].update(new_data)
            updated = True
            break

    if not updated:
        print(f"bot_name '{bot_name}' not found.")
        return

    # write updated data back to file
    try:
        with open(path, 'w') as file:
            yaml.dump_all(data, file, explicit_start=True)
        print(f"updated '{bot_name}' successfully.")
    except IOError as e:
        print(f"Error：{e}")