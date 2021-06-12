import discord
import json
from discord.ext import commands
from datetime import datetime

def now(): return f'[{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}]'

def jsave(path:str, data:dict):
    with open(path, 'w', encoding='utf8') as file:
        json.dump(data, file, sort_keys=True, indent=4, ensure_ascii=False)
    print(f'{now()} Complete save')

def jload(path:str):
    with open(path, 'r') as file:
        data = json.load(file)
    print(f'{now()} Complete load')
    return data

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='mb/', intents=intents)

@bot.event
async def on_ready():
    print(f'{now()} >> Anonymous Mailbox Bot is on ready <<')

@commands.has_guild_permissions(administrator=True)
@bot.group()
async def setting(ctx):
    pass

@setting.command()
async def setup(ctx):
    data = {'input':None, 'Output':None}
    jsave(path='./channel.json', data=data)

@setting.command()
async def Cinput(ctx, channelID:int=None):
    if channelID == None:
        print(f'{now()} [ERROR] The value entered is a null value.')
    elif not ctx.guild.get_channel(channelID):
        print(f'{now()} [ERROR] Channel does not exist')
    else:
        data = jload(path='./channel.json')
        data['input'] = channelID
        jsave(path='./channel.json', data=data)

@setting.command()
async def Coutput(ctx, channelID:int=None):
    if channelID == None:
        print(f'{now()} [ERROR] The value entered is a null value.')
    elif not ctx.guild.get_channel(channelID):
        print(f'{now()} [ERROR] Channel does not exist')
    else:
        data = jload(path='./channel.json')
        data['output'] = channelID
        jsave(path='./channel.json', data=data)

@bot.event
async def on_message(msg):
    data = jload(path='./channel.json')
    if not data['input'] or not data['output']:
        return
    if msg.channel.id == data['input']:
        await msg.delete()
        channel = msg.guild.get_channel(data['output'])
        await channel.send(msg.content)