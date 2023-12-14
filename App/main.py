import json
import os
import discord
import requests
import DB.dbFuncs as db
import Other_Functions.prefix as prefix
import User.profile as profile
import Beatmap.recent as recent
import Beatmap.best as best
import Beatmap.top as top
import Beatmap.track as track
import Beatmap.pp as pp

# Start tracker
import Beatmap.trackFunc as tf

# Reading config file to get the tokens
curPath = os.path.dirname(__file__)
configPath = os.path.join(curPath, "Config/config.json")
configFile = open(configPath)
config = json.load(configFile)
configFile.close()

# Global variables
pref = "??"
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
k = response['access_token']

# Defining client
class Client(discord.Client):
    async def on_ready(self):
        global pref
        pref = db.getPrefix()
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global pref
        content = message.content.lower()
        user = message.author
        if content.startswith(pref):
            command = content.lstrip(pref)
            command = command.split()
            match command[0]:
                case "prefix":
                    await prefix.printPrefix(message.channel)
                case "setprefix":
                    if len(command)==1:
                        command.append(None)
                    pref = await prefix.newPrefix(message.channel,command[1])
                case "profile":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,False)
                case "p":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,False)
                case "ctb":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,False)
                case "profile+":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,True)
                case "p+":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,True)
                case "ctb+":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await profile.printProfile(message.channel,command[1:],k,api,True)
                case "setprofile":
                    if len(command)==1:
                        command.append(None)
                    await profile.newprofile(message.channel,command[1],user.id)
                case "r":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await recent.printRecent(message.channel,command[1:],k,api,message)
                case "rs":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await recent.printRecent(message.channel,command[1:],k,api,message)
                case "recent":
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    await recent.printRecent(message.channel,command[1:],k,api,message)
                case "c":
                    map=None
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    else:
                        for i in command:
                            if i.startswith("m:"):
                                map=i[2:]
                                command[command.index(i)]=command[command.index(i)][2:]
                        if map!=None:
                            command = [x for x in command if x!=map]
                            if len(command)==1:
                                command.append(None)
                                command.append(user.id)
                    await best.printBest(message.channel,command[1:],map,k,api,message)
                case "sc":
                    map=None
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    else:
                        for i in command:
                            if i.startswith("m:"):
                                map=i[2:]
                                command[command.index(i)]=command[command.index(i)][2:]
                        if map!=None:
                            command = [x for x in command if x!=map]
                            if len(command)==1:
                                command.append(None)
                                command.append(user.id)
                    await best.printBest(message.channel,command[1:],map,k,api,message)
                case "score":
                    map=None
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    else:
                        for i in command:
                            if i.startswith("m:"):
                                map=i[2:]
                                command[command.index(i)]=command[command.index(i)][2:]
                        if map!=None:
                            command = [x for x in command if x!=map]
                            if len(command)==1:
                                command.append(None)
                                command.append(user.id)
                    await best.printBest(message.channel,command[1:],map,k,api,message)
                case "top":
                    rec = False
                    page = 1
                    if len(command)==1:
                        command.append(None)
                        command.append(user.id)
                    else:
                        for i in command:
                            if i=="-r":
                                rec = True
                            elif i.startswith("-") and i[1:].isdigit():
                                page = int(i[1:])
                        if rec:
                            command = [x for x in command if x!="-r"]
                        if page!=1:
                            command = [x for x in command if not x.startswith("-") or not x[1:].isdigit()]
                        if len(command)==1:
                            command.append(None)
                            command.append(user.id)
                    await top.printTop(message.channel,command[1:],rec,page,k,api,message)
                case "track":
                    if len(command)==1:
                        command.append(None)
                    await track.setTrack(message.channel,message.channel.id,command[1:],k,api)
                case "stop-track":
                    if len(command)==1:
                        command.append(None)
                    await track.stopTrack(message.channel,message.channel.id,command[1:],k,api)
                case "pp":
                    map=None
                    if len(command)==1:
                        map=None
                        mods=None
                    if len(command)==2:
                        map=command[1]
                        mods=None
                    if len(command)==3:
                        for i in range(len(command)):
                            if command[i].startswith("m:"):
                                mods=command[i][2:]
                            else:
                                map=command[i]
                    await pp.getpp(message.channel,map,mods,k,api)

# Config intents
intents = discord.Intents.default()
intents.message_content = True

# Establishing a new discord client to initialize the bot
client = Client(intents=intents)

tf.setClient(client)

# Running bot
client.run(config["BOT_TOKEN"])