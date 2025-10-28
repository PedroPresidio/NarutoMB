import discord
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from discord.ext import commands
import rolls
from database import *

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGODB_TOKEN = os.getenv("MONGODB_TOKEN")

# Rename the Mongo client variable to avoid colliding with the bot class name
mongo_client = MongoClient(MONGODB_TOKEN)
db = mongo_client["FavListDB"]


class client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            # sync the global app command tree
            await self.tree.sync()
            self.synced = True

        print(f"We are online as {self.user}.")


aclient = client()

aclient.run(TOKEN)

