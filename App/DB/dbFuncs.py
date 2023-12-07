import DB.db as db
import requests
import json
import discord

# API funcs

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

def getRecent(username,key,api):
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

def getTop(username,key,api,offset,limit):
    url = f"{api}users/{username}/scores/best"
    k = f"Bearer {key}"
    params = {
        "include_fails":"1",
        "mode":"fruits",
        "limit":limit,
        "offset":offset
    }
    res = requests.get(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

def getTopRecent(username,key,api,offset,limit):
    url = f"{api}users/{username}/scores/recent"
    k = f"Bearer {key}"
    params = {
        "include_fails":"1",
        "mode":"fruits",
        "limit":limit,
        "offset":offset
    }
    res = requests.get(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

# DB funcs

def getMap(channel,message):
    try:
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
    except:
        return "Err"

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
    try:
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
    except:
        return "Err"

# Function to return a message when a db error occurs

async def err(channel):
    message = discord.Embed(
        title = "Uh oh, error inesperado",
        description = "Reintenta en unos segundos, si no funciona contacta con Alex ;3",
        color = 0x000000
    )
    await channel.send(embed=message)

# Connect database
conn = db.connect()

# Create cursor for using the database
database = conn.cursor()