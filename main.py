# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
import utilities as u
from pymongo import MongoClient
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["DnD"]
charCol = db["Characters"]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(help="does")
async def do(ctx):
    response = "done"
    await ctx.send(response)

@bot.command(help="lets you roll up to 10 dice, with however many sides you want")
async def roll(ctx, num_dice:int = 1, num_sides:int = 6):
    response = u.rolling(num_dice, num_sides)
    await ctx.send(response)

@bot.command(help="create your character. Enter a name when you do it\n"+
    ">create [name]")
async def start(ctx, name = "dumb idiot didn't put a name in"):
    def check(m):
        stats = m.content.split()
        retVal = len(stats) == 6 and m.author == ctx.author
        return retVal
    try:
        await ctx.send("Enter Stats for \"" + name + "\" in the format:\n"+
        "[Str] [Dex] [Con] [Int] [Wis] [Cha]")

        author = await bot.wait_for('message', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('k bye')
    else:
        if(author):
            stats = author.content.split()
            charDict = {"user": ctx.author.id, "name": name, "str": stats[0], "dex": stats[1], "con": stats[2], "int": stats[3], "wis": stats[4], "cha": stats[5]}
            charCol.replace_one({"user": ctx.author.id}, charDict, True)
            await ctx.send('Created')
        else:
            await ctx.send("Oh seems that was too hard for you, try again later")

@bot.command(help="Check all characters in the database")
async def myChar(ctx):
    x = charCol.find_one({"user": ctx.author.id})
    await ctx.send(x)

@bot.command(help="For figuring out who to recommend to your friends")
async def isAjayInRelationship(ctx):
    await ctx.send("no")

bot.run(TOKEN)