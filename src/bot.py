import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ["PREFIX"], intents=intents)
moderator_role_id = int(os.environ["MODERATOR_ROLE_ID"])
admin_role_id = int(os.environ["ADMIN_ROLE_ID"])


def generate_mbed_context(title: str, description: str, colour: discord.colour.Colour) -> discord.embeds.Embed:
    mbed = discord.Embed(title=title,
                         description=description,
                         colour=colour)
    return mbed


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=generate_mbed_context(
            title="ბრძანება",
            description="```მსგავსი ბრძანებისთვის ლოგიკა არ დაუწერია ჯერ არავის.```",
            colour=discord.Colour.dark_red()
        ))
    elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=generate_mbed_context(
            title="არგუმენტები",
            description="```არგუმენტ(ებ)ი არასწორია```",
            colour=discord.Colour.dark_red()
        ))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=generate_mbed_context(
            title="უფლებები",
            description="```თქვენ არ გაქვთ ამ ბრძანებით სარგებლობის უფლება.```",
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
