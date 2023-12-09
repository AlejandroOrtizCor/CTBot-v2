import DB.dbFuncs as db
import discord
    
async def printProfile(channel,username,key,api,plus):
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
            await db.err(channel)
            return None
    else:
        username = " ".join(username)
    profile = db.getProfile(username,key,api)
    if "error" in profile.keys():
        message = discord.Embed(
            title = "Usuario no encontrado",
            description = "El usuario no pudo ser encontrado, revisa el nombre :3",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    title = f"osu!ctb profile for {profile['username']}"
    url = f"https://osu.ppy.sh/users/{profile['id']}"
    rank = f"**Rank:** #{profile['statistics']['global_rank']} (:flag_{profile['country_code'].lower()}: #{profile['statistics']['rank']['country']})"
    pp = f"**PP:** {profile['statistics']['pp']:,}"
    acc = f"**Acc:** {float(profile['statistics']['hit_accuracy']):.4f}%"
    level = f"**Level:** {profile['statistics']['level']['current']} + {profile['statistics']['level']['progress']}%"
    playcount = f"**Playcount:** {profile['statistics']['play_count']:,} ({int(profile['statistics']['play_time'])//3600} hrs)"
    grade = f"<:rankingXH:1028374879973683250>: {profile['statistics']['grade_counts']['ssh']} <:rankingSH:1028374905596682321>: {profile['statistics']['grade_counts']['sh']} <:rankingX:1028374894905413693>: {profile['statistics']['grade_counts']['ss']} <:rankingS:1028374918322208779>: {profile['statistics']['grade_counts']['s']} <:rankingA:1028374929533571205>: {profile['statistics']['grade_counts']['a']}"
    kudosu = f"**Kudosu:** {profile['kudosu']['total']}"
    score = f"**Total score:** {profile['statistics']['total_score']:,} - **Ranked score:** {profile['statistics']['ranked_score']:,}"
    hits = f"**Total hits:** {profile['statistics']['total_hits']:,} - **Max combo:** {profile['statistics']['maximum_combo']:,}"
    if profile['is_online']:
        on = ":green_circle: En línea"
    else:
        on = ":red_circle: Desconectado"
    if plus:
        data = f"{rank}\n{pp}\n{acc}\n{hits}\n{level}\n{playcount}\n{score}\n{kudosu}\n\n{grade}\n\n{on}"
    else:
        data = f"{rank}\n{pp}\n{acc}\n{level}\n{playcount}\n\n{grade}\n\n{on}"
    thumbnail = profile['avatar_url']
    message = discord.Embed(
        title = title,
        url = url,
        description = data,
        color = 0x000000
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(embed=message)

async def newprofile(channel,username,user):
    new = set(user,username)
    if username==None:
        message = discord.Embed(
            title = "Agrega un perfil para linkear",
            description = "Si no agregas un perfil para linkear a tu cuenta de osu no podras hacer uso de todas las funciones de CTBot :pensive:",
            color = 0x000000
        )
        await channel.send(embed=message)
        return None
    if new == "Err":
        await db.err(channel)
        return None
    if new:
        title = "Agregado nuevo usuario :D"
    else:
        title = "Usuario editado correctamente :face_with_monocle:"
    data = "Puedes cambiarlo cuando quieras con el mismo comando, para ver tu perfil puedes poner el comando `??p` o `??p+` para información extra"
    message = discord.Embed(
        title = title,
        description = data,
        color = 0x000000
    )
    await channel.send(embed=message)