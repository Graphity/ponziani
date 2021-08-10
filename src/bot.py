import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(
            title="CommandNotFound",
            description=f"```{error}```",
            colour=discord.Colour.dark_red()
        ))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            title="MissingRequiredArgument",
            description=f"```{error}```",
            colour=discord.Colour.dark_red()
        ))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=discord.Embed(
            title="BadArgument",
            description=f"```{error}```",
            colour=discord.Colour.dark_red()
        ))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="MissingPermissions",
            description=f"```{error}```",
            colour=discord.Colour.dark_red()
        ))
    raise error


@bot.command()
async def ping(ctx):
    await ctx.send(f"pong: {round(bot.latency * 1000)}MS")


for filename in os.listdir("./src/cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ["TOKEN"])
