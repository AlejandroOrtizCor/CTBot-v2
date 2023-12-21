import DB.db as db
import requests
import json
import discord

# API funcs

def getProfile(username,key,api):
    url = f"{api}users/{username}/fruits"
    k = f"Bearer {key}"
    res = requests.get(url,headers={"Authorization":k})
    response = json.loads(res.text)

    return response

def getMapData(mapid,key,api):
    url = f"{api}beatmaps/{mapid}"
    k = f"Bearer {key}"
    params = {
        "mode":"fruits"
    }
    res = requests.get(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

def getMapSr(mapid,key,api,mods):
    url = f"{api}beatmaps/{mapid}/attributes"
    k = f"Bearer {key}"
    params = {
        "ruleset":"fruits",
        "mods":mods
    }
    res = requests.post(url,headers={"Authorization":k},params=params)
    response = json.loads(res.text)

    return response

def getScore(username,mapid,key,api):
    url = f"{api}beatmaps/{mapid}/scores/users/{username}/all"
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

def getPrefix():
    try:
        database.execute("SELECT prefix FROM configs")
        for p in database:
            prefix = p[0]
        return prefix
    except:
        return "Err"

def setPrefix(newPrefix):
    try:
        database.execute(f"UPDATE configs SET prefix = '{newPrefix}'")
    except:
        return "Err"

def setProfile(id, username):
    try:
        database.execute(f"SELECT profile FROM users WHERE id = '{id}'")
        for p in database:
            database.execute(f"UPDATE users SET profile = '{username}' WHERE id = '{id}'")
            return False
        database.execute(f"INSERT INTO users (id,profile) VALUES ('{id}','{username}')")
        return True
    except:
        return "Err"

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
            else:
                database.execute(f"INSERT INTO map (mapa, server) VALUES ('{mapid}','{message.guild.id}')")
        else:
            database.execute(f"SELECT * FROM map WHERE server = '{message.author.id}'")
            maps = []
            for m in database:
                maps.append(m)
            if len(maps)>0:
                database.execute(f"UPDATE map SET mapa = '{mapid}' WHERE server = '{message.author.id}'")
            else:
                database.execute(f"INSERT INTO map (mapa, server) VALUES ('{mapid}','{message.author.id}')")
    except:
        return "Err"
    
def savetrack(channel,message,profile,mapid):
    try:
        if str(channel.type) == "private":
            return "Err2"
        else:
            database.execute(f"SELECT channel FROM track WHERE user = '{profile['id']}'")
            channels = []
            c = ""
            for i in database:
                channels = eval(i[0])
                c = i[0]
            if len(channels)>0 and message in channels:
                return "Err3"
            elif len(channels)>=0 and message not in channels and c.startswith("["):
                channels.append(message)
                database.execute(f"UPDATE track SET channel = '{str(channels)}' WHERE user = '{profile['id']}'")
                return 0
            database.execute(f"INSERT INTO track (channel,user,global_rank,country_rank,pp,last_map) VALUES ('[{message}]','{profile['id']}','{profile['statistics']['global_rank']}','{profile['statistics']['rank']['country']}','{profile['statistics']['pp']}','{mapid}')")
    except:
        return "Err"
    
def gettracks():
    try:
        database.execute(f"SELECT * FROM track")
        data = []
        for i in database:
            data.append(i)
        return data
    except:
        return "Err"
    
def updatetrack(profile,mapid):
    try:
        database.execute(f"UPDATE track SET global_rank = '{profile['statistics']['global_rank']}', country_rank = '{profile['statistics']['rank']['country']}', pp = '{profile['statistics']['pp']}', last_map = '{mapid}' WHERE user = '{profile['id']}'")
        return 0
    except:
        return "Err"

def stoptrack(channel,message,profile):
    try:
        if str(channel.type) == "private":
            return "Err2"
        else:
            database.execute(f"SELECT channel FROM track WHERE user = '{profile['id']}'")
            channels = []
            for i in database:
                channels = eval(i[0])
            if len(channels)==0 or message not in channels:
                return "Err3"
            elif len(channels)>0 and message in channels:
                channels.remove(message)
                database.execute(f"UPDATE track SET channel = '{str(channels)}' WHERE user = '{profile['id']}'")
                return 0
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
conn.autocommit = True

# Create cursor for using the database
database = conn.cursor()