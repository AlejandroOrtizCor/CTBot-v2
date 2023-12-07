import DB.db as db
import discord
import requests
import json
import User.profile as prof
import Beatmap.plays as pl

def get(username,key,api):
    url = f"{api}users/{username}/scores/recent"
    k = f"Bearer {key}"
    params = {
        "include_fails":"1",
        "mode":"fruits",
        "limit":"1"
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

async def printRecent(channel,username,key,api,msg):
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
    profile = prof.get(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = get(profile['id'],key,api)
    if not isinstance(play,list):
        message = discord.Embed(
            title = "No hay plays :pensive:",
            description = "El usuario no tiene plays recientes",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = play[0]
    savemap(channel,msg,play['beatmap']['beatmapset_id'])
    name = f"**Recent CTB play for {play['user']['username']}:**"
    await pl.printPlay(name,play,channel)

# Connect database
conn = db.connect()

# Create cursor for using the database
database = conn.cursor()