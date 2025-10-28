import discord
from discord import app_commands
from discord.ext import commands
import database


class RollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Show a Pokémon by name and add it to your favorites!")
    @app_commands.describe(pokemon_name="The Pokémon you want to view (e.g., Pikachu)")
    async def roll(self, interaction: discord.Interaction, pokemon_name: str):
        """Fetch a Pokémon from the PokeAPI (via database.get_pokemon_info) and allow the user to favorite it."""
        name = pokemon_name.strip().lower()

        poke = database.get_pokemon_info(name)
        if not poke:
            await interaction.response.send_message(
                f"Pokemon '{pokemon_name}' not found or API error.",
                ephemeral=True
            )
            return

        # Build a friendly description
        desc = f"**Name:** {poke['name'].capitalize()}\n**ID:** {poke['id']}\n**Height:** {poke['height']}\n**Weight:** {poke['weight']}"
        embed = discord.Embed(
            title=f"{poke['name'].capitalize()}",
            description=desc,
            color=discord.Color.blurple()
        )

        view = discord.ui.View()

        async def favorite_callback(interact: discord.Interaction):
            # Use the database helper to add favorite (it is async)
            await database.favoritar(interact.user, poke['name'].capitalize())
            await interact.response.send_message(
                f"⭐ {poke['name'].capitalize()} added to your favorites!",
                ephemeral=True
            )

        fav_button = discord.ui.Button(label="Favorite", style=discord.ButtonStyle.green, emoji="⭐")
        fav_button.callback = favorite_callback
        view.add_item(fav_button)

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(RollCog(bot))
