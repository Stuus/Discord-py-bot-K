import asyncio
import datetime
import discord
import os
import subprocess
import time

from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import voice_recv

from tools.color import Color as C


class StatsSink(voice_recv.AudioSink):
    def __init__(self, filename):
        # use WaveSink to handle actual file writing
        self.wav_sink = voice_recv.WaveSink(filename)
        #  { UserID: { 'packets': 0, 'bytes': 0, 'start_time': float } }
        self.stats = {} 
        self.start_time = time.time()

    def wants_opus(self) -> bool:
        # WaveSink need PCM，return False
        return False

    def write(self, user, data):
        # collect stats
        if user:
            user_id = user.id
            if user_id not in self.stats:
                self.stats[user_id] = {'packets': 0, 'bytes': 0, 'name': user.name}
            
            self.stats[user_id]['packets'] += 1
            self.stats[user_id]['bytes'] += len(data.pcm)

        # write to wav sink
        self.wav_sink.write(user, data)

    def cleanup(self):
        self.wav_sink.cleanup()
        # output stats
        print(f"\n[Recored] total: {time.time() - self.start_time:.2f} second(s)")
        for uid, stat in self.stats.items():
            # 20ms (0.02s)
            duration = stat['packets'] * 0.02
            print(f"User: {stat['name']} | Speak: {duration:.2f}s | packets: {stat['bytes']} bytes")


class CogVoice(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client
    
    @app_commands.command(
        name = "join",
        description = "Make the bot join your voice channel"
    )
    async def join(self, interaction:discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not connected to a voice channel.",ephemeral=True,delete_after=60)
            return
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"Joined {channel}.")

    @app_commands.command(
        name = "record",
        description = "Record audio in voice channel"
    )
    @app_commands.choices(file_types=[
        Choice(name='wav', value=1),
        Choice(name='mp3',  value=2)
    ])
    @app_commands.describe(
        file_types="Select file type to record",
        time="Recording time in seconds (1-600)"
    )
    async def record(
            self,
            interaction: discord.Interaction,
            file_types: Choice[int] = 1,
            time: discord.app_commands.Range[int, 1, 600] = 10,
    ):

        if not interaction.user.voice.channel:
            return await interaction.response.send_message("You are not connected to a voice channel.",ephemeral=True,delete_after=60)
        
        target_channel = interaction.user.voice.channel

        vc = interaction.guild.voice_client

        await interaction.response.send_message(f"Ready to record @ {target_channel} for {time} second(s).")

        if vc is not None:
            # Already connected
            if vc.channel.id == target_channel.id:
                # In the same channel -> stop current recording
                #vc.stop_listening()
                await vc.disconnect()
            else:
                # Other channel -> disconnect first
                await vc.disconnect()
        
        # create a new connection
        try:
            vc = await target_channel.connect(cls=voice_recv.VoiceRecvClient)
        except discord.ClientException:
            # Already connected to a voice channel
            await asyncio.sleep(0.5)
            vc = await target_channel.connect(cls=voice_recv.VoiceRecvClient)
        
        ffmpeg_path = os.path.join("tools", "ffmpeg.exe")
        # Check if ffmpeg exists
        if not os.path.exists(ffmpeg_path):
             await interaction.response.send_message(f"Error: `FFmpeg not found at {ffmpeg_path}`")
             return



        dt = str(datetime.datetime.now())[:-7].replace(" ","_").replace(":","-")
        wav_filename = f'{dt}.wav'
        mp3_filename = f'{dt}.mp3'

        # Start recording
        s_sink = StatsSink(wav_filename)
        vc.listen(sink=s_sink)
        await asyncio.sleep(time)  # Record untill end
        vc.stop_listening()
        stats_msg = "## Statistics: \n```"
        for uid, stat in s_sink.stats.items():
            u = f"User: {stat['name']}"
            s = f"Speak: {stat['packets'] * 0.02:.2f}s"
            p = f"packets: {stat['bytes']} bytes"
            stats_msg += f"{u:<30} | {s:<30} | {p:<30}\n"
        stats_msg += "```"


        if file_types == 1:  # WAV
            msg = (f"{stats_msg}\n## Sound recored as **`{wav_filename}`**")
            await interaction.channel.send(content=msg,file=discord.File(wav_filename))
        
        elif file_types == 2:  # MP3
            if os.path.exists(ffmpeg_path):
                try:
                    command = [
                        ffmpeg_path,              # path to ffmpeg executable
                        '-i', wav_filename,       # input file
                        '-acodec', 'libmp3lame',  # transcode to mp3
                        '-ab', '192k',            # Bitrate
                        '-y',                     # relace output file if exists
                        mp3_filename
                    ]
                    subprocess.run(command, check=True)
                    msg = (f"{stats_msg}\n## Sound recored as **`{mp3_filename}`**")
                    await interaction.channel.send(content=msg,file=discord.File(mp3_filename))
                
                except FileNotFoundError:
                    await interaction.channel.send("FFmpeg not found. Please ensure FFmpeg is installed and the path is correct.")
                except subprocess.CalledProcessError as e:
                    await interaction.channel.send(f"Error during audio conversion: {e} ")

        vc.stop_listening()
        await vc.disconnect()
        # cleanup file
        if os.path.exists(wav_filename):
            os.remove(wav_filename)
            print(f"Removed temporary file: {wav_filename}")
        if os.path.exists(mp3_filename):
            os.remove(mp3_filename)
            print(f"Removed temporary file: {mp3_filename}")


async def setup(client:commands.Bot) -> None:
    await client.add_cog(CogVoice(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.libiue}load cog_voice{C.reset}')