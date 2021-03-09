import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)
moderator_role_id = int(os.environ["MODERATOR_ROLE_ID"])
admin_role_id = int(os.environ["ADMIN_ROLE_ID"])

@bot.event
async def on_ready() :
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to >help"))

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

@bot.command()
@commands.has_any_role(moderator_role_id, admin_role_id)
async def role(ctx, role: discord.Role):
    member = ctx.message.author
    await member.add_roles(role)
    await ctx.send("role granted!")


bot.run(os.environ["TOKEN"])
