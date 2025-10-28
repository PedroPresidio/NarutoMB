import pymongo
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Base URL for PokeAPI
base_url = "https://pokeapi.co/api/v2"

mongo_client = pymongo.MongoClient(os.getenv("MONGODB_TOKEN"))
database = mongo_client["FavListDB"]
favorites_collection = database["favorites"]

def get_pokemon_info(name: str):
    """Return the Pokemon JSON from the API or None on failure."""
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


if __name__ == "__main__":
    pokemon_name = input("Enter the name of the Pokemon: ").lower()
    poke_info = get_pokemon_info(pokemon_name)
    if poke_info:
        print(f"Name: {poke_info['name'].capitalize()}")
        print(f"ID: {poke_info['id']}")
        print(f"Height: {poke_info['height']}")
        print(f"Weight: {poke_info['weight']}")
        print(f"Sprites: {poke_info['sprites']}")


async def novo_usuario(usuario):
    filter = {"discord_id": usuario.id}
    if favorites_collection.count_documents(filter) == 0:
        doc = {"discord_id": usuario.id, "Favorites": []}
        favorites_collection.insert_one(doc)
        return doc
    return False


async def favoritos(usuario):
    await novo_usuario(usuario)
    filter = {"discord_id": usuario.id}
    cursor = favorites_collection.find(filter)
    try:
        return cursor.__getitem__(0)["Favorites"]
    except Exception:
        return []


async def favoritar(usuario, card: str):
    await novo_usuario(usuario)
    filter = {"discord_id": usuario.id}
    fav = await favoritos(usuario)
    favorites_collection.update_one(filter, {"$set": {"Favorites": fav + [card]}})


