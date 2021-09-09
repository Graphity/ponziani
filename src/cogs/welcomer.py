import os
import requests
import random
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🤖"

    def avatar(self, member):
        if member.avatar:
            return member.avatar
        return member.default_avatar

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = os.environ.get("WELCOME_CHANNEL", 841223740456697856)
        channel = member.guild.get_channel(int(channel_id))
        self.create_card(member.name, channel.guild.name, channel.guild.member_count, self.avatar(member))
        await channel.send(f'{member.mention} just joined the server', file=discord.File("welcome.png"))

    @commands.command()
    @commands.is_owner()
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        os.environ["WELCOME_CHANNEL"] = str(channel.id)

    def create_card(self, member_name, guild_name, member_count, member_avatar_url):
        background = Image.new("RGB", (1100, 500), color=(9, 10, 11))
        background_draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("/app/.fonts/Hack-Bold.ttf", 45)
        font_color = random.choice(["#ee4540", "#85daff", "#429fa4", "#ff813c", "#9580ff", "#8aff80", "#ffff80", "#004aac"])
        background_draw.text((550, 320), f"Hello {member_name}", fill=font_color, font=font, anchor="mt")
        background_draw.text((550, 380), f"Welcome to {guild_name}", fill=font_color, font=font, anchor="mt")
        background_draw.text((550, 440), f"Member #{member_count}", fill=font_color, font=font, anchor="mt")

        r = requests.get(member_avatar_url)
        avatar = Image.open(BytesIO(r.content)).convert("RGB").resize((260, 260))
        mask = Image.new("L", avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
        border = Image.new("RGB", (avatar.size[0]+12, avatar.size[1]+12), color=(9, 10, 11))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse((0, 0, avatar.size[0]+12, avatar.size[1]+12), fill=(35, 39, 42))
        border.paste(avatar, (6, 6), mask)

        background.paste(border, (408, 20))
        background.filter(ImageFilter.SMOOTH)
        background.save("welcome.png")
    
    @commands.command()
    @commands.is_owner()
    async def test_welcomer(self, ctx, member: discord.User=None):
        if not member:
            member = ctx.author
        channel_id = os.environ.get("WELCOME_CHANNEL", 841223740456697856)
        channel = ctx.guild.get_channel(int(channel_id))
        self.create_card(member.name, ctx.guild.name, ctx.guild.member_count, self.avatar(member))
        await channel.send(file=discord.File("welcome.png"))


def setup(bot):
    bot.add_cog(Welcomer(bot))
