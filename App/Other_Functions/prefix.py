import DB.dbFuncs as db
import discord

async def printPrefix(channel):
    prefix = db.getPrefix()
    if prefix=="Err":
        await db.err(channel)
        return None
    data = f"Prefijo: `{prefix}`\nSi deseas cambiarlo usa el comando `{prefix}setprefix prefijo`"
    message = discord.Embed(
        title = "Prefijo CTBot",
        description = data,
        color = 0x000000
    )
    await channel.send(embed=message)

async def newPrefix(channel,newPrefix):
    oldPrefix = db.getPrefix()
    if oldPrefix=="Err":
        await db.err(channel)
        return None
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
        n=db.setPrefix(newPrefix)
        if n=="Err":
            await db.err(channel)
            return None
        data = f"Se cambió el prefijo `{oldPrefix}` a `{newPrefix}`"
    message = discord.Embed(
        title = "Prefijo CTBot",
        description = data,
        color = 0x000000
    )
    await channel.send(embed=message)
    return newPrefix