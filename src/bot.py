import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)
moderator_role_id = int(os.environ["MODERATOR_ROLE_ID"])
admin_role_id = int(os.environ["ADMIN_ROLE_ID"])


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("მსგავსი ბრძანებისთვის ლოგიკა არ დაუწერია ჯერ არავის")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("არგუმენტ(ებ)ი არასწორია")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Sike!")
    raise error

@bot.command()
async def ping(ctx):
    await ctx.send(f"pong: {round(bot.latency * 1000)}MS")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.environ["TOKEN"])
