import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ['PREFIX'], intents=intents)

@bot.event
async def on_ready():
    game = discord.Game(f'{bot.command_prefix}help')
    await bot.change_presence(activity=game)
    print('Ready!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('მსგავსი ბრძანებისთვის ლოგიკა არ დაუწერია ჯერ არავის')
    raise error

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong: {round(bot.latency * 1000)}MS')


bot.run(os.environ['TOKEN'])
