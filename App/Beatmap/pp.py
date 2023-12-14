import DB.dbFuncs as db
import discord
import Other_Functions.pp as pp
import Other_Functions.parsemods as parsemods

async def getpp(channel,map,mods,key,api):
    if map==None:
        message = discord.Embed(
            title = "Pon un mapa",
            description = "Para ver el pp de un mapa, debes poner el mapa, ya sea su link o id",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    if map.isdigit():
        mapid = map
    else:
        mapid = map[map.find("#fruits/")+8:]
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