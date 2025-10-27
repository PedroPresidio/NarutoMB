import pymongo 
from dotenv import load_dotenv
import os

load_dotenv()

client  = pymongo.MongoClient("MTQzMjM3OTQxNDY5OTgzNTQ4NQ.GJz7S8.UInNAx5KjQXFOpWAo9VrGowq4wNZl1vFGXC1-I")
bancodedados = client["economia"]
usuarios = bancodedados ["usuarios"]

async def novo_usuario(usuario):
    filter = {"discord_id": usuario.id}
    if usuario.count_documents(filter) == 0:
        object = {
            "discord_id":usuario.id,
            "coins" :100            
        }
    else:
        return False

async def checar_saldo(usuario):

    await novo_usuario(usuario)

    filtro = {"discord_id": usuario.id}
    resultado = usuario.find(filter)

    return resultado.__getitem__(0)["moedas"]

async def alterar_saldo(usuario, quantidade):
    await novo_usuario(usuario)
    current_balance = await checar_saldo(usuario)

    filter = {"discord_id":usuario.id}
    reation = {
        "$set": {"coins": current_balance+quantidade}
    }


