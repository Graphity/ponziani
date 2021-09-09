from discord.ext import commands
import discord
import os


class RolesButton(discord.ui.Button["Roles"]):
    def __init__(self, name, emoji):
        if emoji:
            super().__init__(label=name, emoji=emoji)
        else:
            super().__init__(label=name, style=1)

    async def callback(self, interaction: discord.Interaction):
        roles = await interaction.guild.fetch_roles()
        member = await interaction.guild.fetch_member(interaction.user.id)
        for role in roles:
            if role.name == self.label:
                if role in member.roles:
                    await member.remove_roles(role)
                else:
                    await member.add_roles(role)
                return

class Roles(discord.ui.View):
    def __init__(self, roles):
        super().__init__()
        for name, emoji in roles.items():
            self.add_item(RolesButton(name, emoji))


class RolesBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🤖"

    @commands.command()
    @commands.is_owner()
    async def roles(self, ctx):
        config = await self.bot.get_config()
        roles_channel = await self.bot.fetch_channel(os.environ["ROLES_CHANNEL_ID"])
        await roles_channel.purge()
        for roles in config["roles"]:
            if isinstance(roles, list):
                roles = {name:None for name in roles}
            await roles_channel.send("\u200b", view=Roles(roles))


def setup(bot):
    bot.add_cog(RolesBot(bot))
