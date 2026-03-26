import datetime
import discord

from discord import Message
from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo

class CogListener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def _get_msg_content(self, message: Message) -> str:
        if len(message.embeds) >= 1:
            return message.embeds[0].title or "No Title"
        elif len(message.attachments) >= 1:
            return '\n'.join(att.url for att in message.attachments)
        return message.content or str(message)

    async def log_message(self, message: Message, action_prefix: str, color_code: str, discord_log_fmt: str, before_message: Message = None):
        guild_name = message.guild.name if message.guild else f"DM-{message.author.name}"
            
        output_channel = self.client.get_channel(ConfigInfo.listener_id)
        if message.channel == output_channel:
            return

        now = str(datetime.datetime.now())[:-7]
        
        msg = self._get_msg_content(message)
        if len(message.embeds) >= 1:
            tmp = f'  {color_code}{action_prefix}embed : [{msg}]{C.reset}'
        elif len(message.attachments) >= 1:
            tmp = f'  {color_code}{action_prefix}URL : \n{msg}\n{C.reset}'
        else:
            tmp = f'  {color_code}{action_prefix}say : {msg}{C.reset}'

        # output to console
        out = f'{C.gray}{now} {C.blue}[{guild_name}]  {C.reset}@{message.channel}  {C.red}{message.author.name}{C.reset}'
        print(out + tmp)

        # send in msg channel
        if output_channel is not None:
            format_kwargs = {
                "now": now,
                "guild": guild_name,
                "channel": message.channel,
                "author": message.author.name,
                "msg": msg
            }
            if before_message:
                format_kwargs["b_msg"] = self._get_msg_content(before_message)
                format_kwargs["a_msg"] = msg

            discord_out = discord_log_fmt.format(**format_kwargs)
            await output_channel.send(discord_out)
        elif ConfigInfo.listener_id is not None:
            print(f"{C.red}Warning: output channel not found for listener.{C.reset}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.log_message(
            message, 
            "", 
            C.lightblue, 
            "**{now}** `{guild}` `{channel}`  **{author}**  :  {msg} "
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        await self.log_message(
            after,
            "edit ", 
            C.purple, 
            "**{now} UTC+0** `{guild}` `{channel}`  **{author}** msg edit : \n    {b_msg}\n    {a_msg} ",
            before_message=before
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        await self.log_message(
            message, 
            "delete ", 
            C.red, 
            "**{now}** `{guild}` `{channel}`  **{author}**  msg delete:  {msg} "
        )


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogListener(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.lightblue}load cog_listener{C.reset}')