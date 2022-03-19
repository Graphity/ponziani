from discord.ext import commands
import discord


class Polls(commands.Cog):
    letters = [
        "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
        "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
    ]
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "📊"

    @commands.command()
    async def poll(self, ctx, question, *options):
        """Makes poll"""
        description = ""
        for i in range(len(options)):
            description += f"\n{self.letters[i]} **{options[i]}**"
        poll = discord.Embed(title=question, description=description)
        poll.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        msg = await ctx.send(embed=poll)
        for i in range(len(options)):
            await msg.add_reaction(self.letters[i])
        await ctx.message.delete()

    @commands.command()
    async def simplepoll(self, ctx, *question):
        """Makes simple poll (Yes or No question)"""
        poll = discord.Embed(description=f"```{' '.join(question)}```")
        poll.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        msg = await ctx.send(embed=poll)
        await msg.add_reaction(self.bot.get_emoji(878398674454069319))
        await msg.add_reaction(self.bot.get_emoji(878398709883367466))
        await ctx.message.delete()

    @commands.command()
    async def question(self, ctx, msg_id: int, *new_question):
        """Changes poll question"""
        msg = await ctx.fetch_message(msg_id)
        if msg.embeds:
            if ctx.author.name != msg.embeds[0].author.name:
                await ctx.send("You have to be author of the poll to change it\"s question")
                return
        poll_dict = msg.embeds[0].to_dict()
        if poll_dict.get("title"):
            poll_dict["title"] = " ".join(new_question)
        else:
            poll_dict["description"] = f"```{' '.join(new_question)}```"
        await msg.edit(embed=discord.Embed.from_dict(poll_dict))

    @commands.command()
    async def option(self, ctx, msg_id: int, emoji, *new_option):
        """Changes one specific option of the poll"""
        msg = await ctx.fetch_message(msg_id)
        if msg.embeds:
            if ctx.author.name != msg.embeds[0].author.name:
                await ctx.send("You have to be author of the poll to change it\"s option")
                return        
        poll_dict = msg.embeds[0].to_dict()
        options = poll_dict["description"].split("\n")
        for option in options:
            if option.startswith(emoji):
                poll_dict["description"] = poll_dict["description"].replace(option, f"{emoji} **{' '.join(new_option)}**")
                await msg.edit(embed=discord.Embed.from_dict(poll_dict))
                return

    @commands.command()
    async def addoption(self, ctx, msg_id: int, *new_option):
        """Adds new poll option"""
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        new_option_id = len(poll_dict["description"].split("\n"))
        poll_dict["description"] += f"\n{self.letters[new_option_id]} **{' '.join(new_option)}**"
        await msg.edit(embed=discord.Embed.from_dict(poll_dict))
        await msg.add_reaction(self.letters[new_option_id])


async def setup(bot):
    await bot.add_cog(Polls(bot))
