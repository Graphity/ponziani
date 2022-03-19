from discord.ext import commands
import discord
import json
import os


class Administer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🔒"

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
        reason = " ".join(reason)
        await ctx.message.delete()
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Log: Ban",
            description=f"```Banned {member.name}\nreason: {reason}```",
            colour=discord.Colour.dark_red()
        )
        log_channel = await self.bot.fetch_channel(os.environ["LOG_CHANNEL_ID"])
        await log_channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        reason = " ".join(reason)        
        await ctx.message.delete()
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Log: Kick",
            description=f"```Kicked {member.name}\nreason: {reason}```",
            colour=discord.Colour.dark_red()
        )
        log_channel = await self.bot.fetch_channel(os.environ["LOG_CHANNEL_ID"])
        await log_channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def activity(self, ctx, activity_type, *name):
        """Changes activity. (Possible ActivityTypes: listening, watching, playing)"""
        try:
            activity_type = {
                "listening": discord.ActivityType.listening,
                "watching": discord.ActivityType.watching,
                "playing": discord.ActivityType.playing,
            }[activity_type]
        except:
            return
        activity = discord.Activity(type=activity_type, name=" ".join(name))
        await self.bot.change_presence(activity=activity)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add_prefix(self, ctx, prefix):
        if prefix in ["'", '"']:
            await ctx.send("I can't add that prefix")
            return
        config = await self.bot.get_config()
        guild_id = str(ctx.guild.id)
        if guild_id in config["prefixes"]:
            config["prefixes"][guild_id].append(prefix)
        else:
            config["prefixes"][guild_id] = [prefix]
        config_json = json.dumps(config, indent=4)
        with open("config.json", "w") as f:
            f.write(config_json)
        config_channel = await self.bot.fetch_channel(os.environ["CONFIG_CHANNEL_ID"])
        await config_channel.send(file=discord.File("config.json"))
        self.bot.prefixes = config["prefixes"]


async def setup(bot):
    await bot.add_cog(Administer(bot))
