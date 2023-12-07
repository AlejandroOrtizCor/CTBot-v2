import discord

async def printPlay(name,play,channel):
    if len(play['mods'])==0:
        mods = "No Mod"
    else:
        mods = "".join(play['mods'])
    title = f"{play['beatmapset']['title']} [{play['beatmap']['version']}] + {mods} [{play['beatmap']['difficulty_rating']}★]"
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
    data = f"{rank} - {pp} - {acc}\n{score} - {combo} - {stats}"
    message = discord.Embed(
        title = title,
        url = url,
        description = data,
        color = 0x0099FF
    )
    message.set_thumbnail(url=thumbnail)
    await channel.send(name,embed=message)