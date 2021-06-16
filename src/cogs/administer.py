import os

import discord
from discord.ext import commands


class Administer(commands.Cog):

    def __init__(self, bot):
        """
        Init
        :param bot: Runner Class
        """
        self.client = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int) -> None:
        """შლის შეტყობინებების კონკრეტულ რაოდენობას."""

        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None) -> None:
        """ბანი."""

        mbed = discord.Embed(
            title="Success",
            description=f"ბანი დაედო მომხმარებელს: {member.display_name}",
        )
        await ctx.send(embed=mbed)
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None) -> None:
        """გაგდება."""

        await member.kick(reason=reason)

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def load(self, ctx, extension) -> None:
        """კოგის ინსტალაცია."""

        self.client.load_extension(f"cogs.{extension}")
        mbed = discord.Embed(title="COGS",
                             description=f"Loaded cog: {extension}.",
                             colour=discord.Colour.dark_red())
        await ctx.send(embed=mbed)

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def unload(self, ctx, extension) -> None:
        """კოგის დეინსტალაცია."""

        self.client.unload_extension(f"cogs.{extension}")
        mbed = discord.Embed(title="COGS",
                             description=f"```Unloaded cog: {extension}```",
                             colour=discord.Colour.dark_red())
        await ctx.send(embed=mbed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # TODO ERROR HANDLING METHODS BELOW                 #
    # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @staticmethod
    def generate_mbed_context(title: str, description: str, colour: discord.colour.Colour) -> discord.embeds.Embed:
        mbed = discord.Embed(title=title,
                             description=description,
                             colour=colour)
        return mbed

    # @clear.error
    # async def clear_error(self, ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         mbed = discord.Embed(title="ბრძანებსი არასწორი სინტაქსი",
    #                              description="```$clear <რაოდენობა>```",
    #                              colour=discord.Colour.dark_red())
    #         await ctx.send(embed=mbed)

    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            mbed = self.generate_mbed_context(
                title="COGS",
                description="```ინსტალაცია ვერ ხერხდება: უკვე დაინსტალირებულია.```",
                colour=discord.Colour.dark_red())

            await ctx.send(embed=mbed)

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            mbed = self.generate_mbed_context(
                title="COGS",
                description="```დეინსტალაცია ვერ ხერხდება: უკვე დეინსტალირებულია.```",
                colour=discord.Colour.dark_red())
            await ctx.send(embed=mbed)


def setup(bot) -> None:
    """Cog setup."""

    bot.add_cog(Administer(bot))
