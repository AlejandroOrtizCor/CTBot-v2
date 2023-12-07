import DB.dbFuncs as db
import discord
import User.profile as prof
import Beatmap.plays as pl

async def printTop(channel,username,recent,page,key,api,msg):
    if username[0] == None or username[0].startswith("<@"):
        if username[0] != None:
            username.append(username[0][2:-1])
        username = db.getfromdb(username[1])
        if username == None:
            message = discord.Embed(
                title = "Linkea un usuario a tu cuenta de discord",
                description = "Para linkear un usuario escribe el comando `??setprofile username` y listo :D",
                color = 0x000000
            )
            await channel.send(embed=message)
            return None
        elif username == "Err":
            message = discord.Embed(
                title = "Uh oh, error inesperado",
                description = "Reintenta en unos segundos, si no funciona contacta con Alex ;3",
                color = 0x000000
            )
            await channel.send(embed=message)
            return None
    else:
        username = " ".join(username)
    offset = (page-1)*5
    limit = 5
    profile = prof.get(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    if recent:
        top = db.getTopRecent(profile['id'],key,api,offset,limit)
    else:
        top = db.getTop(profile['id'],key,api,offset,limit)
    name = f"**Best CTB plays for {profile['username']}:**"
    url = f"https://osu.ppy.sh/users/{profile['id']}"
    thumbnail = profile['avatar_url']
    titleTotal = f"Top Catch the Beat! Plays for {profile['username']}"
    await pl.printTop(name,url,thumbnail,titleTotal,top,channel)