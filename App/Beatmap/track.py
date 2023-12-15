import DB.dbFuncs as db
import discord
from datetime import datetime

async def setTrack(channel,msg,username,key,api):
    if username[0]==None:
        message = discord.Embed(
            title = "Pon un nombre de usuario",
            description = "Para trackear un jugador, pon su username despues del comando, asi: `??track username` :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    else:
        username = " ".join(username)
    profile = db.getProfile(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    offset = 0
    limit = 100
    top = db.getTop(profile['id'],key,api,offset,limit)
    for p in range(len(top)):
        top[p]['r'] = p+1
    dateFormat = "%Y-%m-%dT%H:%M:%SZ"
    top.sort(key=lambda p: datetime.strptime(p['created_at'],dateFormat),reverse=True)
    save = db.savetrack(channel,msg,profile,top[0]['id'])
    if save=="Err":
        await db.err(channel)
        return None
    elif save=="Err2":
        message = discord.Embed(
            title = "No se puede trackear en DM",
            description = "Debes trackear usuarios en servidores, no en DM",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    elif save=="Err3":
        message = discord.Embed(
            title = "Ya se esta trackeando",
            description = "Este usuario ya se esta trackeando en este canal",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    message = discord.Embed(
        title = "Usuario trackeado exitosamente :3",
        description = f"El usuario `{profile['username']}` será trackeado en este canal. Para dejar de trackearlo pon el comando `??stop-track username` :3",
        color = 0x000000
    )
    await channel.send(embed=message)

async def stopTrack(channel,msg,username,key,api):
    if username[0]==None:
        message = discord.Embed(
            title = "Pon un nombre de usuario",
            description = "Para dejar de trackear un jugador, pon su username despues del comando, asi: `??stop-track username` :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    else:
        username = " ".join(username)
    profile = db.getProfile(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    stop = db.stoptrack(channel,msg,profile)
    if stop=="Err":
        await db.err(channel)
        return None
    elif stop=="Err2":
        message = discord.Embed(
            title = "No se puede trackear en DM",
            description = "Debes trackear usuarios en servidores, no en DM",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    elif stop=="Err3":
        message = discord.Embed(
            title = "No se está trackeando",
            description = "Este usuario no se esta trackeando en este canal",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    message = discord.Embed(
        title = "Comando ejecutrado exitosamente :3",
        description = f"El usuario `{profile['username']}` ya no será trackeado en este canal. Para volver trackearlo pon el comando `??track username` :3",
        color = 0x000000
    )
    await channel.send(embed=message)