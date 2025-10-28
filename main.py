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
        # sync commands (prefer guild sync for development when GUILD_ID is set)
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

        # Debug: list registered app commands
        try:
            cmds = list(self.tree.get_commands())
            print(f"Registered app commands ({len(cmds)}): {[c.name for c in cmds]}")
        except Exception as e:
            print("Could not list commands:", e)

        print(f"We are online as {self.user}.")


aclient = client()

# Add cogs so slash commands defined in them are registered
aclient.add_cog(rolls.RollCog(aclient))

aclient.run(TOKEN)

