import discord
from discord import app_commands
from discord.ext import commands
from main import *  

favorites_collection = db["favorites"]

class FavoritesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="favorites", description="See your list of favorite Pokémon!")
    async def favorites(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = favorites_collection.find_one({"user_id": user_id})

        if user_data and "favorites" in user_data and len(user_data["favorites"]) > 0:
            favs = ", ".join(user_data["favorites"])
            await interaction.response.send_message(f"⭐ Your favorite Pokémon: {favs}")
        else:
            await interaction.response.send_message("You don’t have any favorites yet! Use `/roll` to add one!")

async def setup(bot):
    await bot.add_cog(FavoritesCog(bot))
