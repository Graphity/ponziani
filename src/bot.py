from discord.ext import commands
import discord
import json
import os


def _get_prefix(bot, msg):
    if msg.guild:
        return bot.get_guild_prefixes(msg.guild.id)
    return "."


class Ponziani(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=_get_prefix,
            intents=discord.Intents.all(),
            help_command=None
        )

        for filename in os.listdir("./src/cogs"):
            name, extension = os.path.splitext(filename)
            if extension == ".py":
                try:
                    self.load_extension(f"cogs.{name}")
                except:
                    print(f"Failed to load extension: {filename}")

    def get_guild_prefixes(self, guild_id):
        guild_id = str(guild_id)
        if guild_id in self.prefixes:
            prefixes = self.prefixes[str(guild_id)]
            return [".", *prefixes]
        return "."

    async def get_config(self):
        channel = await self.fetch_channel(os.environ["CONFIG_CHANNEL_ID"])
        messages = await channel.history(limit=1).flatten()
        c = await messages[0].attachments[0].read()
        return json.loads(c)
        
    async def on_command_error(self, ctx, error):
        await ctx.send(embed=discord.Embed(
            title=type(error).__name__,
            description=f"```{error}```",
            colour=discord.Colour.red()
        ))
        raise error

    async def on_ready(self):
        config = await self.get_config()
        self.prefixes = config["prefixes"]
        self.get_cog("Dev").emoji = self.get_emoji(877225723025317949)
        print("Ready...")


if __name__ == "__main__":
    bot = Ponziani()
    bot.run(os.environ["TOKEN"])
