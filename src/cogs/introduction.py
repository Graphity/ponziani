import discord
from discord.ext import commands


class Introduction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_repo = "https://github.com/Graphity/it-georgia"
        self.invite_link = discord.utils.oauth_url(client_id=str(bot.user.id), permissions=discord.Permissions(permissions=8))

    @commands.Cog.listener()
    async def on_ready(self):
        listening = discord.Activity(type=discord.ActivityType.listening, name=f"{self.bot.command_prefix}help")
        await self.bot.change_presence(activity=listening)
        print("Ready...")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id in message.raw_mentions:
            embed = discord.Embed(
                title="",
                type="rich",
                description=f"**Prefix:** `{self.bot.command_prefix}`",
                color=0x49329e,
                url="https://github.com/Graphity/it-georgia"
            )
            embed.set_author(
                name=self.bot.user.name,
                url=self.invite_link
            )
            embed.set_thumbnail(
                url=self.bot.user.avatar_url
            )
            await message.channel.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(self.invite_link)

    @commands.command()
    async def source(self, ctx):
        await ctx.send(self.github_repo)


def setup(bot):
    bot.add_cog(Introduction(bot))
