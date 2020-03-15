# bot.py
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(help="does the only command in the bot")
async def do(ctx):
    response = "done"
    await ctx.send(response)

@bot.command(help="rolls a dice or multiple")
async def roll(ctx, num_dice = '1', num_sides = '6'):
    dice_n = int(num_dice)
    dice_s = int(num_sides)
    if(dice_n < 1 or dice_n > 10):
        response = "haha"
    else:
        response = "Rolled Number(s):"
        total = 0
        for i in range(dice_n):
            num = random.randint(1, dice_s)
            response = response + "  " + str(num)
            total += num
        if int(num_dice) > 1:
            response = response + "\nTotal: " + str(total)
    await ctx.send(response)

bot.run(TOKEN)