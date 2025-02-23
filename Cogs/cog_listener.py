import datetime
import discord

from discord import Message
from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo

cid = ConfigInfo.listener_id


class CogListener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message:Message):
        #get message
        oput_channel = self.client.get_channel(cid)
        if message.channel == oput_channel:
            return

        else:
            now = str(datetime.datetime.now())[:-7]
            if len(message.embeds) >= 1:
            #get embrd
                tmp = (f'  {C.libiue}embed : [{message.embeds[0].title}]{C.reset}')
                msg = (f'{message.embeds[0].title}')

            elif len(message.attachments) >= 1:
            #get picture[URL]
                urls = ('')
                for i in range(len(message.attachments)):
                    urls = urls + '\n' + message.attachments[i].url
                tmp = (f'  {C.libiue}URL : \n{urls}\n{C.reset}')
                msg = (f'{urls}')


            else:
            #context
                tmp = (f'  {C.libiue}say : {message.content}{C.reset}')
                msg = (f'{message.content}')

            #outpute
            out = (f'{C.gray}{now} {C.blue}[{message.guild.name}]  {C.reset}@{message.channel}  {C.red}{message.author.name}{C.reset}')
            print(out+tmp)
            


            #send in msg channel
            try:
                out = (f'**{now}** `{message.guild.name}` `{message.channel}`  **{message.author.name}**  :  {msg} ')
                await oput_channel.send(out)
            except AttributeError:
                pass



    @commands.Cog.listener()
    async def on_message_edit(self, before:Message, after:Message):
    #get message [edit]
        oput_channel = self.client.get_channel(cid)
        if after.channel == oput_channel:
            return

        else:
            now = str(datetime.datetime.now())[:-7]
            if len(after.embeds) >= 1:
            #embed
                tmp = (f'  {C.purple}edit embed : [{after.embeds[0].title}]{C.reset}')
                msg = (f'{after.embeds[0].title}')

            elif len(after.attachments) >= 1:
            #get picture[URL]
                urls = ('')
                for i in range(len(after.attachments)):
                    urls = urls + '\n' + after.attachments[i].url
                tmp = (f'  {C.purple}edit URL : \n{urls}\n{C.reset}')
                msg = (f'{urls}')

            else:
            #context
                tmp = (f'  {C.purple}edit say : {after.content}{C.reset}')
                msg = (f'{after}')

            #outpute
            out = (f'{C.gray}{now} {C.blue}[{after.guild.name}]  {C.reset}@{after.channel}  {C.red}{after.author.name}{C.reset}')
            print(out+tmp)



            #send in msg channel
            try:
                out = (f'**{now} UTC+0** `{after.guild.name}` `{after.channel}`  **{after.author.name}** msg edit :  {msg} ')
                await oput_channel.send(out)
            except AttributeError:
                pass
            



    @commands.Cog.listener()
    async def on_message_delete(self, message:Message):
    #get message[delete]

        oput_channel = self.client.get_channel(cid)

        if message.channel == oput_channel:
            return

        else:
            now = str(datetime.datetime.now())[:-7]
            if len(message.embeds) >= 1:
            #embed
                tmp = (f'  {C.red}delete embed : [{message.embeds[0].title}]{C.reset}')
                msg = (f'{message.embeds[0].title}')

            elif len(message.attachments) >= 1:
            #get picture[URL]
                urls = ('')
                for i in range(len(message.attachments)):
                    urls = urls + '\n' + message.attachments[i].url
                tmp = (f'  {C.red}delete URL : \n{urls}\n{C.reset}')
                msg = (f'{urls}')

                
            else:
            #context
                tmp = (f'  {C.red}delete say : {message.content}{C.reset}')
                msg = (f'{message.content}')
            
            #outpute
            out = (f'{C.gray}{now} {C.blue}[{message.guild.name}]  {C.reset}@{message.channel}  {C.red}{message.author.name}{C.reset}')
            print(out+tmp)
            
            #send in msg channel
            try:
                out = (f'**{now}** `{message.guild.name}` `{message.channel}`  **{message.author.name}**  msg delete:  {msg} ')
                await oput_channel.send(out)
            except AttributeError:
                pass


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogListener(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_listener{C.reset}')