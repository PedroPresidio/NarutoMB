import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from database import *

class client(discord.client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        print (f"We are online as {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(name = "balance", description= "Check you Balance")
async def balance(interaction: discord.Integration):
    coins = await checar_saldo(interaction.user)
    await interaction.response.send_message(f"You have a balance of {coins}")

aclient.run(os.getenv("BOT_TOKEN"))