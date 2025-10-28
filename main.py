import discord
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from discord.ext import commands
import functions.rolls as rolls
from database import *
import functions.favorite as favorite

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MONGODB_TOKEN = os.getenv("MONGODB_TOKEN")

mongo_client = MongoClient(MONGODB_TOKEN)
db = mongo_client["FavListDB"]


class client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
        self.synced = False

    async def setup_hook(self) -> None:
        """Called by discord.py before the connection is made. Add cogs here with await."""
        # Add cogs here so they are registered before sync/on_ready
        await self.add_cog(rolls.RollCog(self))
        await self.add_cog(favorite.FavoritesCog(self))

    async def on_ready(self):
        
        if not self.synced:
            guild_id = os.getenv("GUILD_ID")
            if guild_id:
                try:
                    guild_obj = discord.Object(id=int(guild_id))
                    await self.tree.sync(guild=guild_obj)
                    print(f"Synced commands to guild {guild_id}")
                except Exception as e:
                    print("Guild sync failed:", e)
            else:
                try:
                    await self.tree.sync()
                    print("Synced global commands")
                except Exception as e:
                    print("Global sync failed:", e)

            self.synced = True


aclient = client()

aclient.run(TOKEN)

