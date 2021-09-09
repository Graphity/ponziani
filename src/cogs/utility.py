from discord.ext import commands
import discord


class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="List of Command Groups",
            description=f"To view the commands in each group use:\n```.help <group>```",
            colour=0x3172d9
        )
        for cog, commands in mapping.items():
            if not cog or len(commands) == 0:
                continue

            try:
                emoji = f"{cog.emoji} "
            except:
                emoji = ""

            embed.add_field(
                name=f"{emoji}**{cog.qualified_name}**",
                value=f"{len(commands)} commands"
            )
        await self.get_destination().send(embed=embed)            

    async def send_cog_help(self, cog):
        commands = cog.get_commands()
        if len(commands) == 0:
            await self.get_destination().send("Cog has 0 commands")
            return
        
        msg = "```asciidoc"
        sep = len(max([command.name for command in commands], key=len)) + 2
        for command in commands:
            msg += f"\n• {command.name}{' ' * (sep-len(command.name))}:: {command.help if command.help else ''}"
        msg += f"```\nUse `.help <command>`for help with specific command"
        await self.get_destination().send(msg)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=command.name.upper(),
            description=f"{command.help if command.help else ''}",
            color=0x3172d9
        )
        embed.add_field(name="Format:", value=f"```{self.get_command_signature(command)}```")
        await self.get_destination().send(embed=embed)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔧'
        self.bot.help_command = CustomHelpCommand()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong: {round(self.bot.latency * 1000)}MS")

    @commands.command()
    @commands.guild_only()
    async def emoji(self, ctx, *names):
        """Sends any emoji from any server bot is connected to (No Nitro Required)"""
        converter = commands.EmojiConverter()
        content = ""
        for name in names:
            emoji = await converter.convert(ctx, name)
            content += str(emoji)
        await ctx.message.delete()
        await ctx.send(content)

    @commands.command()
    @commands.guild_only()
    async def react(self, ctx, msg_id, *names):
        """Reacts with any emoji from any server bot is connected to (No Nitro Required)"""
        converter = commands.EmojiConverter()
        msg = await ctx.fetch_message(msg_id)
        for name in names:
            emoji = await converter.convert(ctx, name)
            await msg.add_reaction(emoji)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def prefixes(self, ctx):
        await ctx.send(f"`{self.bot.get_guild_prefixes(ctx.guild.id)}`")


def setup(bot):
    bot.add_cog(Utility(bot))
