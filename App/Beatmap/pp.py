import DB.dbFuncs as db
import discord
import Other_Functions.pp as pp
import Other_Functions.parsemods as parsemods

async def getpp(channel,map,mods,key,api,msg):
    if map==None:
        mapid = db.getMap(channel,msg)
        if mapid == "Err":
            await db.err(channel)
            return None
        if mapid == "":
            message = discord.Embed(
                title = "Error",
                description = "No hay un mapa anteriormente mencionado en este server, menciona uno usando un `??rs` antes o un `??c mapa` o `??c usario mapa`",
                color = 0x000000
            )
            await channel.send(embed=message)
            return None
    elif map.isdigit():
        mapid = map
    elif "#fruits/" in map:
        mapid = map[map.find("#fruits/")+8:]
    elif "beatmaps/" in map:
        mapid = map[map.find("beatmaps/")+9:]
    if mods!=None:
        mods=mods.split(",")
    else:
        mods=[]
    mapdata = db.getMapData(mapid,key,api)
    modsint = parsemods.parse(mods)
    sr = db.getMapSr(mapid,key,api,modsint)
    sr = sr['attributes']['star_rating']
    total = pp.calcpp(sr,mapdata['ar'],mapdata['max_combo'],mods)
    if len(mods)==0:
        mods="No Mod"
    else:
        mods = [mod.upper() for mod in mods]
        mods = "".join(mods)
    title = f"{mapdata['beatmapset']['title']} [{mapdata['version']}] + {mods}"
    url = mapdata['url']
    desc = f"**100%** - {total[0]} PP\n**99%** - {total[1]} PP\n**98%** - {total[2]} PP"
    thumbnail = f"https://b.ppy.sh/thumb/{mapdata['beatmapset_id']}l.jpg"
    message = discord.Embed(
        title = title,
        description = desc,
        url = url,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(embed=message)