import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ['PREFIX'], intents=intents)

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to >help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('მსგავსი ბრძანებისთვის ლოგიკა არ დაუწერია ჯერ არავის')
    raise error

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong: {round(bot.latency * 1000)}MS')

@client.command()
async def role(ctx, role: discord.Role):
  member = ctx.message.author
  await member.add_roles(role)
  await ctx.send(f"role granted!")


bot.run(os.environ['TOKEN'])
