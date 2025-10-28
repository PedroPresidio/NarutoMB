import discord
from discord import app_commands
from discord.ext import commands
import database


class FavoritesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="favorites", description="See your list of favorite Pokémon!")
    async def favorites(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = database.favorites_collection.find_one({"discord_id": user_id})

        if user_data and "Favorites" in user_data and len(user_data["Favorites"]) > 0:
            favs = ", ".join(user_data["Favorites"]) if isinstance(user_data["Favorites"], list) else str(user_data["Favorites"])
            await interaction.response.send_message(f"Your Pokémon list: {favs}")
        else:
            await interaction.response.send_message("You do not have any favorites yet! Use `/roll` to add one!")


async def setup(bot):
    await bot.add_cog(FavoritesCog(bot))
