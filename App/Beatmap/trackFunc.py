import time
import threading
import DB.dbFuncs as db
from datetime import datetime
import os
import json
import requests
import asyncio
import discord
import Other_Functions.parsemods as parsemods

# Reading config file to get the tokens
curPath = os.path.dirname(__file__)
configPath = os.path.join(curPath, "../Config/config.json")
configFile = open(configPath)
config = json.load(configFile)
configFile.close()

# Vars
api = "https://osu.ppy.sh/api/v2/"
url = "https://osu.ppy.sh/oauth/token"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}
body = {
    "client_id":config['client_id'],
    "client_secret":config['client_secret'],
    "grant_type":"client_credentials",
    "scope":"public"
}
res = requests.post(url,headers=headers,data=body)
response = json.loads(res.text)
key = response['access_token']

client = 0

def setClient(c):
    global client
    client = c

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            pass
        next_time += (time.time() - next_time) // delay * delay + delay

def getMsg(name,play,track,profile):
    if len(play['mods'])==0:
        mods = "No Mod"
    else:
        mods = "".join(play['mods'])
    modsint = parsemods.parse(play['mods'])
    sr = db.getMapSr(play['beatmap']['id'],key,api,modsint)
    sr = sr['attributes']['star_rating']
    title = f"**New {play['r']})** {play['beatmapset']['title']} [{play['beatmap']['version']}] + {mods} [{sr:.2f}★]"
    url = play['beatmap']['url']
    if play['rank'] == "XH":
        rank = "<:rankingXH:1028374879973683250>"
    elif play['rank'] == "X":
        rank = "<:rankingX:1028374894905413693>"
    elif play['rank'] == "SH":
        rank = "<:rankingSH:1028374905596682321>"
    elif play['rank'] == "S":
        rank = "<:rankingS:1028374918322208779>"
    elif play['rank'] == "A":
        rank = "<:rankingA:1028374929533571205>"
    elif play['rank'] == "B":
        rank = "<:rankingB:1028374941625753710>"
    elif play['rank'] == "C":
        rank = "<:rankingC:1028374952354795550>"
    elif play['rank'] == "D":
        rank = "<:rankingD:1028374963297726535>"
    elif play['rank'] == "F":
        rank = "F"
    acc = f"{(float(play['accuracy'])*100):.2f}%"
    if play['pp'] == None:
        pp = "**0.00 PP**"
    else:
        pp = f"**{float(play['pp']):.2f} PP**"
    score = f"{play['score']:,}"
    combo = f"x{play['max_combo']}/{int(play['statistics']['count_100'])+int(play['statistics']['count_300'])+int(play['statistics']['count_miss'])}"
    stats = f"[{play['statistics']['count_300']}/{play['statistics']['count_100']}/{play['statistics']['count_50']}/{play['statistics']['count_miss']}]"
    thumbnail = f"https://b.ppy.sh/thumb/{play['beatmap']['beatmapset_id']}l.jpg"
    changes = f"**PP:** {float(track[4]):,} PP -> {profile['statistics']['pp']:,} PP\n**Global rank:** #{track[1]} -> #{profile['statistics']['global_rank']}\n**Country rank:** #{track[2]} -> #{profile['statistics']['rank']['country']}"
    dateFormat = "%Y-%m-%dT%H:%M:%SZ"
    d = datetime.strptime(play['created_at'],dateFormat)
    d = int(time.mktime(d.timetuple()))
    date = f"<t:{d}:F>"
    data = f"{rank} - {pp} - {acc}\n{score} - {combo} - {stats}\n{changes}\n{date}"
    message = discord.Embed(
        title = title,
        url = url,
        description = data,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    return [name, message]

async def printTrack(channel, name, message):
    await channel.send(name,embed=message)

def check():
    tracks = db.gettracks()
    if tracks == "Err":
        print("Error")
        return 0
    for track in tracks:
        username = track[3]
        profile = db.getProfile(username,key,api)
        offset = 0
        limit = 100
        top = db.getTop(profile['id'],key,api,offset,limit)
        for p in range(len(top)):
            top[p]['r'] = p+1
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        top.sort(key=lambda p: datetime.strptime(p['created_at'],dateFormat),reverse=True)
        if str(profile['statistics']['pp'])==track[4]:
            continue
        if str(top[0]['id'])==track[5]:
            continue
        update = db.updatetrack(profile,top[0]['id'])
        if update == "Err":
            print("Error")
            continue
        name = f"**Recent CTB play for {profile['username']}:**"
        chns = eval(track[0])
        for id in chns:
            channel = client.get_channel(id)
            msg = getMsg(name,top[0],track,profile)
            asyncio.run_coroutine_threadsafe(printTrack(channel,msg[0],msg[1]),client.loop)

def getkey():
    global key
    url = "https://osu.ppy.sh/oauth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {
        "client_id":config['client_id'],
        "client_secret":config['client_secret'],
        "grant_type":"client_credentials",
        "scope":"public"
    }
    res = requests.post(url,headers=headers,data=body)
    response = json.loads(res.text)
    key = response['access_token']

threading.Thread(target=lambda: every(86000, getkey)).start()
threading.Thread(target=lambda: every(5, check)).start()