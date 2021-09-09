from discord.ext import commands
import discord


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        await ctx.send("https://github.com/Graphity/ponziani")

    @commands.command()
    async def aboutemoji(self, ctx, *emojis):
        """Sends some useful info of emoji(s)"""
        converter = commands.EmojiConverter()
        for emoji in emojis:
            info = f"Encoded :: {emoji.encode('ascii', 'namereplace')}"
            try:
                e = await converter.convert(ctx, emoji)
            except:
                continue
            else:
                info += f"\nEmojiID :: {e.id}\nURL     :: {e.url}"
            finally:
                await ctx.send(f"```asciidoc\n{info}```")

    @commands.command()
    async def embed_to_dict(self, ctx, msg_id):
        """Converts embed to dictionary"""
        msg = await ctx.fetch_message(msg_id)
        await ctx.send(f"```{msg.embeds[0].to_dict()}```")


def setup(bot):
    bot.add_cog(Dev(bot))
