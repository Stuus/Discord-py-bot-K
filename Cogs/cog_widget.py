import os
import json
import datetime
import discord
import aiohttp
from discord import app_commands
from discord.ext import commands

from tools.color import Color as C


__dependencies__ = [
    "user_config.json"
]

class CogWidget(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.config_path = "user_config.json"

    def load_config(self) -> dict:
        """Reads variables dynamically from the configuration file."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # --------------------------------------------------
    # Command: /widget-setup
    # --------------------------------------------------
    @app_commands.command(
        name="widget-setup",
        description="Setup and authorize your custom Discord profile widget"
    )
    async def widget_setup(self, interaction: discord.Interaction):
        try:
            config = self.load_config()
            app_id = config.get("application_id")
            
            # Generate the specific OAuth2 URL for widget authorization
            oauth2_url = f"https://discord.com/oauth2/authorize?client_id={app_id}&response_type=token&scope=openid+sdk.social_layer"
            
            # Create a UI View with an authorization button
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Authorize Widget", url=oauth2_url, style=discord.ButtonStyle.link))
            
            await interaction.response.send_message(
                "Please click the button below to authorize this application to update your widget. Once authorized, use `/widget-refresh`.", 
                view=view, 
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"Setup failed: {str(e)}", ephemeral=True)

    # --------------------------------------------------
    # Command: /widget-refresh
    # --------------------------------------------------
    @app_commands.command(
        name="widget-refresh",
        description="Sync and push the latest data to your profile widget"
    )
    async def widget_refresh(self, interaction: discord.Interaction):
        # Defer response since API calls might take longer than 3 seconds
        await interaction.response.defer(ephemeral=True)
        try:
            config = self.load_config()
            app_id = config.get("application_id")
            bot_token = config.get("bot_token")
            # Fetch dynamic image URL from config
            image_url = config.get("image_url") 

            user_id = interaction.user.id
            
            # Construct the exact JSON payload required by Discord
            payload = {
                "username": f"kuro_{user_id}", 
                "data": {
                    "dynamic": [
                        {
                            "type": 3,
                            "name": "0",
                            "value": {
                                "url": image_url
                            }
                        }
                    ]
                }
            }
            
            url = f"https://discord.com/api/v9/applications/{app_id}/users/{user_id}/identities/0/profile"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bot {bot_token}",
                "User-Agent": "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)"
            }
            # Execute asynchronous PATCH request
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, json=payload, headers=headers) as response:
                    if response.status in (200, 204):
                        await interaction.followup.send("✅ Widget successfully updated! Please check your profile.", ephemeral=True)
                    else:
                        error_text = await response.text()
                        status_code = response.status
                        reason = response.reason
                        
                        if not error_text.strip():
                            error_text = "Empty Response"
                            
                        await interaction.followup.send(
                            f"❌ Failed (HTTP {status_code} {reason}):\n{error_text}", 
                            ephemeral=True
                        )
                        
        except Exception as e:
            await interaction.followup.send(f"❌ System error occurred: {str(e)}", ephemeral=True)

# 3. Module load entry point required by Kuroshio
async def setup(client: commands.Bot) -> None:
    await client.add_cog(CogWidget(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.lightblue}load cog_widget{C.reset}')