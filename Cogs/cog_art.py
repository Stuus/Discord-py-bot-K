import datetime
import discord
import os
import PIL


from discord import app_commands
from discord.ext import commands
from PIL import Image

from tools.color import Color as C


class CogArt(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(
            name='to_ascii',
            type=discord.AppCommandType.message,
            callback=self.to_ascii
        )
        self.client.tree.add_command(self.ctx_menu)
    
    async def to_ascii(self, interaction: discord.Interaction, message: discord.Message):
            if len(message.attachments) >= 1:
                attachment = message.attachments[0]
                try:
                    os.remove('./assets/tmp/img.png')
                except FileNotFoundError:
                    pass
                await attachment.save(fp='./assets/tmp/img.png')
                result = f"```\n{image_to_ascii(image_path='assets/tmp/img.png',output_width=50)}\n```"
                await interaction.response.send_message(content=result)
            else:
                await interaction.response.send_message(content="No attachments found in the message.")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogArt(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_Art{C.reset}')

def image_to_ascii(image_path, output_width=75)-> str:
    ASCII_CHARS = '   .-=*co+etilI#hFHER$0@'
    
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        return f"Error: Image file not found at {image_path}"
    img = img.convert('L') 

    width, height = img.size
    aspect_ratio = height/width
    new_height = int(output_width * aspect_ratio * 0.55)
    img = img.resize((output_width, new_height))

    char_step_size = 256 / len(ASCII_CHARS) 
    
    pixels = img.getdata()
    ascii_str = ''
    
    for pixel_value in pixels:
        index = int(pixel_value // char_step_size)
        ascii_str += ASCII_CHARS[index]

    ascii_img = ''
    for i in range(0, len(ascii_str), output_width):
        ascii_img += ascii_str[i:i + output_width] + '\n'
    return ascii_img