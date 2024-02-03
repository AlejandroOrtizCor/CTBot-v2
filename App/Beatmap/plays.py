import discord
from datetime import datetime
import time
from Other_Functions.parsemods import parse as parsemods
import DB.dbFuncs as db
from Other_Functions.pp import calcpp

async def printPlay(name,play,channel,sr,key,api):
    mapdata = db.getMapData(play['beatmap']['id'],key,api)
    modsint = parsemods(play['mods'])
    sr = db.getMapSr(play['beatmap']['id'],key,api,modsint)
    total = calcpp(sr['attributes']['star_rating'],sr['attributes']['approach_rate'],mapdata['max_combo'],play['mods'])
    sr = sr['attributes']['star_rating']
    if len(play['mods'])==0:
        mods = "No Mod"
    else:
        mods = "".join(play['mods'])
    title = f"{play['beatmapset']['title']} [{play['beatmap']['version']}] + {mods} [{sr:.2f}★]"
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
    combo = f"x{play['max_combo']}/{play['maximum']}"
    stats = f"[{play['statistics']['count_300']}/{play['statistics']['count_100']}/{play['statistics']['count_50']}/{play['statistics']['count_miss']}] (Droplets: {play['statistics']['count_katu']})"
    thumbnail = f"https://b.ppy.sh/thumb/{play['beatmap']['beatmapset_id']}l.jpg"
    fc = f"({total[0]} PP for 100%)"
    dateFormat = "%Y-%m-%dT%H:%M:%SZ"
    d = datetime.strptime(play['created_at'],dateFormat)
    d = int(time.mktime(d.timetuple()))
    date = f"<t:{d}:D>"
    data = f"{rank} - {pp} - {acc} - {fc}\n{score} - {combo} - {stats}\n{date}"
    message = discord.Embed(
        title = title,
        url = url,
        description = data,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(name,embed=message)

async def printTop(name,urlTotal,thumbnail,titleTotal,top,channel,key,api):
    titles = []
    dataTotal = []
    for play in top:
        if len(play['mods'])==0:
            mods = "No Mod"
        else:
            mods = "".join(play['mods'])
        url = play['beatmap']['url']
        modsint = parsemods(play['mods'])
        sr = db.getMapSr(play['beatmap']['id'],key,api,modsint)
        sr = sr['attributes']['star_rating']
        title = f"**{play['r']})** [{play['beatmapset']['title']} [{play['beatmap']['version']}] + {mods} [{sr:.2f}★]]({url})"
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
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        d = datetime.strptime(play['created_at'],dateFormat)
        d = int(time.mktime(d.timetuple()))
        date = f"<t:{d}:D>"
        data = f"{rank} - {pp} - {acc}\n{score} - {combo} - {stats}\n{date}"
        titles.append(title)
        dataTotal.append(data)
    final = []
    for d in range(len(dataTotal)):
        final.append(titles[d])
        final.append(dataTotal[d])
        final.append(" ")
    final="\n".join(final)
    message = discord.Embed(
        title = titleTotal,
        url = urlTotal,
        description = final,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(name,embed=message)

async def printBest(name,urlTotal,thumbnail,titleTotal,top,channel,key,api):
    titles = []
    dataTotal = []
    for play in top:
        if len(play['mods'])==0:
            mods = "No Mod"
        else:
            mods = "".join(play['mods'])
        modsint = parsemods(play['mods'])
        sr = db.getMapSr(play['beatmap']['id'],key,api,modsint)
        sr = sr['attributes']['star_rating']
        title = f"**{play['r']}) {mods}** [{sr:.2f}★]"
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
        combo = f"x{play['max_combo']}/{play['maximum']}"
        stats = f"[{play['statistics']['count_300']}/{play['statistics']['count_100']}/{play['statistics']['count_50']}/{play['statistics']['count_miss']}]"
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        d = datetime.strptime(play['created_at'],dateFormat)
        d = int(time.mktime(d.timetuple()))
        date = f"<t:{d}:D>"
        data = f"{rank} - {pp} - {acc}\n{score} - {combo} - {stats}\n{date}"
        titles.append(title)
        dataTotal.append(data)
    final = []
    for d in range(len(dataTotal)):
        final.append(titles[d])
        final.append(dataTotal[d])
        final.append(" ")
    final="\n".join(final)
    message = discord.Embed(
        title = titleTotal,
        url = urlTotal,
        description = final,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(name,embed=message)