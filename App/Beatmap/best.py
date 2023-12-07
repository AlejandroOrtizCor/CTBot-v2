import DB.db as db
import discord
import requests
import json
import User.profile as prof
import Beatmap.plays as pl

def getMap(channel,message):
    maps = ""
    if str(channel.type) != "private":
        database.execute(f"SELECT mapa FROM map WHERE server = '{message.guild.id}'")
        maps = ""
        for m in database:
            maps = m[0]
    else:
        database.execute(f"SELECT mapa FROM map WHERE server = '{message.author.id}'")
        maps = ""
        for m in database:
            maps = m[0]
    
    return maps

def getMapData(mapid,key,api):
    url = f"{api}beatmaps/{mapid}"
    k = f"Bearer {key}"
    params = {
        "mode":"fruits"
    }
    res = requests.get(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

def getScore(username,mapid,key,api):
    url = f"{api}beatmaps/{mapid}/scores/users/{username}"
    k = f"Bearer {key}"
    params = {
        "mode":"fruits"
    }
    res = requests.get(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

def getfromdb(id):
    try:
        database.execute(f"SELECT profile FROM users WHERE id = '{id}'")
        name = ""
        for p in database:
            name = p[0]
        if name!="":
            return name
        else:
            return None
    except:
        return "Err"

def savemap(channel,message,mapid):
    if str(channel.type) != "private":
        database.execute(f"SELECT * FROM map WHERE server = '{message.guild.id}'")
        maps = []
        for m in database:
            maps.append(m)
        if len(maps)>0:
            database.execute(f"UPDATE map SET mapa = '{mapid}' WHERE server = '{message.guild.id}'")
            conn.commit()
        else:
            database.execute(f"INSERT INTO map (mapa, server) VALUES ('{mapid}','{message.guild.id}')")
            conn.commit()
    else:
        database.execute(f"SELECT * FROM map WHERE server = '{message.author.id}'")
        maps = []
        for m in database:
            maps.append(m)
        if len(maps)>0:
            database.execute(f"UPDATE map SET mapa = '{mapid}' WHERE server = '{message.author.id}'")
            conn.commit()
        else:
            database.execute(f"INSERT INTO map (mapa, server) VALUES ('{mapid}','{message.author.id}')")
            conn.commit()

async def printBest(channel,username,key,api,msg):
    if username[0] == None or username[0].startswith("<@"):
        if username[0] != None:
            username.append(username[0][2:-1])
        username = getfromdb(username[1])
        if username == None:
            message = discord.Embed(
                title = "Linkea un usuario a tu cuenta de discord",
                description = "Para linkear un usuario escribe el comando `??setprofile username` y listo :D",
                color = 0x0099FF
            )
            await channel.send(embed=message)
            return None
        elif username == "Err":
            message = discord.Embed(
                title = "Uh oh, error inesperado",
                description = "Reintenta en unos segundos, si no funciona contacta con Alex ;3",
                color = 0x0099FF
            )
            await channel.send(embed=message)
            return None
    else:
        username = " ".join(username)
    mapid = getMap(channel,msg)
    if mapid == "":
        message = discord.Embed(
            title = "Error",
            description = "No hay un mapa anteriormente mencionado en este server, menciona uno usando un `??rs` antes o un `??c mapa` o `??c usario mapa`",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    mapdata = getMapData(mapid,key,api)
    profile = prof.get(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = getScore(profile['id'],mapid,key,api)
    if "error" in play.keys():
        message = discord.Embed(
            title = "No hay plays :pensive:",
            description = "El usuario no tiene plays en este mapa",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = play['score']
    play['beatmapset'] = mapdata['beatmapset']
    savemap(channel,msg,play['beatmap']['beatmapset_id'])
    name = f"**Best CTB play for {play['user']['username']}:**"
    await pl.printPlay(name,play,channel)

# Connect database
conn = db.connect()

# Create cursor for using the database
database = conn.cursor()