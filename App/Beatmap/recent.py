import DB.dbFuncs as db
import discord
import User.profile as prof
import Beatmap.plays as pl

async def printRecent(channel,username,key,api,msg):
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
            await db.err(channel)
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
    play = db.getRecent(profile['id'],key,api)
    if not isinstance(play,list):
        message = discord.Embed(
            title = "No hay plays :pensive:",
            description = "El usuario no tiene plays recientes",
            color = 0x0099FF
        )
        await channel.send(embed=message)
        return None
    play = play[0]
    mapdata = db.getMapData(play['beatmap']['id'],key,api)
    play['maximum'] = mapdata['max_combo']
    e = db.savemap(channel,msg,play['beatmap']['id'])
    if e == "Err":
        await db.err(channel)
        return None
    name = f"**Recent CTB play for {play['user']['username']}:**"
    await pl.printPlay(name,play,channel)