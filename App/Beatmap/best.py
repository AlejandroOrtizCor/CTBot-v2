import DB.dbFuncs as db
import discord
import User.profile as prof
import Beatmap.plays as pl

async def printBest(channel,username,map,key,api,msg):
    if username[0] == None or username[0].startswith("<@"):
        if username[0] != None:
            username.append(username[0][2:-1])
        username = db.getfromdb(username[1])
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
    if map==None:
        mapid = db.getMap(channel,msg)
        if mapid == "Err":
            await db.err(channel)
            return None
        if mapid == "":
            message = discord.Embed(
                title = "Error",
                description = "No hay un mapa anteriormente mencionado en este server, menciona uno usando un `??rs` antes o un `??c mapa` o `??c usario mapa`",
                color = 0x0099FF
            )
            await channel.send(embed=message)
            return None
    else:
        if map.isdigit():
            mapid = map
        else:
            mapid = map[map.find("#fruits/")+8:]
    mapdata = db.getMapData(mapid,key,api)
    if "error" in mapdata.keys():
        message = discord.Embed(
            title = "Mapa no encontrado",
            description = "El mapa no pudo ser encontrado, verifica que el mapa sea de ctb o convert, y revisa el link o id :3",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    profile = prof.get(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = db.getScore(profile['id'],mapid,key,api)
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
    play['maximum'] = mapdata['max_combo']
    e = db.savemap(channel,msg,play['beatmap']['id'])
    if e == "Err":
        await db.err(channel)
        return None
    name = f"**Best CTB play for {play['user']['username']}:**"
    await pl.printPlay(name,play,channel)