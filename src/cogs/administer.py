from discord.ext import commands
import discord


class Administer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int, user: discord.Member=None):
        if amount < 1:
            await ctx.send("Min amount = 1")
            return
        if amount > 100:
            await ctx.send("Max amount = 100")
            return

        if not user:
            try:
                await ctx.channel.purge(limit=amount+1)
            except Exception as e:
                await ctx.send(e)
            return

        if user == ctx.author:
            amount += 1

        messages_to_delete = []
        while True:
            async for message in ctx.channel.history():
                if amount == 0:
                    try:
                        await ctx.channel.delete_messages(messages_to_delete)
                    except Exception as e:
                        await ctx.send(e)
                    return
                if message.author == user:
                    messages_to_delete.append(message)
                    amount -= 1

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        await ctx.message.delete()
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Log: Ban",
            description=f"```Banned {member.name}\nreason: {reason}```",
            colour=discord.Colour.dark_red()
        )
        log_channel = await self.bot.fetch_channel("LOG_CHANNEL_ID")
        await log_channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        await ctx.message.delete()
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Log: Kick",
            description=f"```Kicked {member.name}\nreason: {reason}```",
            colour=discord.Colour.dark_red()
        )
        log_channel = await self.bot.fetch_channel("LOG_CHANNEL_ID")
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Administer(bot))
