import DB.db as db
import discord

def get():
    database.execute("SELECT prefix FROM configs")
    for p in database:
        prefix = p[0]
    
    return prefix

def set(newPrefix):
    database.execute(f"UPDATE configs SET prefix = '{newPrefix}'")
    conn.commit()

async def printPrefix(channel):
    data = f"Prefijo: `{get()}`\nSi deseas cambiarlo usa el comando `{get()}setprefix prefijo`"
    message = discord.Embed(
        title = "Prefijo CTBot",
        description = data,
        color = 0x000000
    )
    await channel.send(embed=message)

async def newPrefix(channel,newPrefix):
    oldPrefix = get()
    if newPrefix==None:
        data = f"Agrega un prefijo por favor"
        newPrefix = oldPrefix
    elif newPrefix.isalnum():
        data = f"Solo se pueden prefijos de simbolos, no se pueden poner prefijos de numeros o letras"
        newPrefix = oldPrefix
    elif len(newPrefix)>2:
        data = f"Pon un prefijo de 1-2 caracteres por favor"
        newPrefix = oldPrefix
    else:
        set(newPrefix)
        data = f"Se cambió el prefijo `{oldPrefix}` a `{newPrefix}`"
    message = discord.Embed(
        title = "Prefijo CTBot",
        description = data,
        color = 0x000000
    )
    await channel.send(embed=message)
    return newPrefix

# Connect database
conn = db.connect()

# Create cursor for using the database
database = conn.cursor()