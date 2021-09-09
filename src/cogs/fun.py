from discord.ext import commands
import discord
import requests


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "😁"

    def animal_embed(self, endpoint):
        r = requests.get(endpoint).json()
        embed = discord.Embed(
            description=f"Fact: {r['fact']}",
            colour=0x3172d9
        )
        embed.set_image(url=r["image"])
        return embed

    @commands.command()
    async def dog(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/dog"))

    @commands.command()
    async def cat(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/cat"))

    @commands.command()
    async def panda(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/panda"))

    @commands.command()
    async def fox(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/fox"))

    @commands.command()
    async def redpanda(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/red_panda"))
            
    @commands.command()
    async def koala(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/koala"))

    @commands.command()
    async def bird(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/birb"))

    @commands.command()
    async def raccoon(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/raccoon"))

    @commands.command()
    async def kangaroo(self, ctx):
        await ctx.send(embed=self.animal_embed("https://some-random-api.ml/animal/kangaroo"))

    def anime_embed(self, endpoint, description):
        r = requests.get(endpoint).json()
        embed = discord.Embed(
            description=description,
            colour=0x3172d9
        )
        embed.set_image(url=r["link"])
        return embed
    
    @commands.command()
    async def wink(self, ctx, member: discord.Member):
        embed = self.anime_embed("https://some-random-api.ml/animu/wink",
                                 f"{ctx.author.mention} winked at {member.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        embed = self.anime_embed("https://some-random-api.ml/animu/pat",
                                 f"{ctx.author.mention} pats {member.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        embed = self.anime_embed("https://some-random-api.ml/animu/hug",
                                 f"{ctx.author.mention} hugs {member.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        r = requests.get("https://some-random-api.ml/joke").json()
        await ctx.send(r["joke"])

    @commands.command()
    async def meme(self, ctx):
        r = requests.get("https://some-random-api.ml/meme").json()
        embed = discord.Embed(
            description=f"{r['caption']}",
            colour=0x3172d9
        )
        embed.set_image(url=r["image"])
        await ctx.send(embed=embed)

    @commands.command()
    async def token(self, ctx):
        r = requests.get("https://some-random-api.ml/bottoken").json()
        await ctx.send(f"Bot Token: `{r['token']}`")

    def overlay(self, endpoint):
        r = requests.get(endpoint)
        with open("image.png", "wb") as f:
            f.write(r.content)
        return discord.File("image.png")

    def avatar(self, member):
        if member.avatar:
            return member.avatar
        return member.default_avatar
    
    @commands.command()
    async def gay(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/gay?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def glass(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/glass?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def wasted(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/wasted?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def passed(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/passed?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def jail(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/jail?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def comrade(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/comrade?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def triggered(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/triggered?avatar={self.avatar(member)}")
        await ctx.send(file=image)
    
    @commands.command()
    async def pixelate(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/pixelate?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def blur(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/blur?avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def ytcomment(self, ctx, comment, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/youtube-comment?username={member.name}&comment={comment}&avatar={self.avatar(member)}")
        await ctx.send(file=image)

    @commands.command()
    async def tweet(self, ctx, comment, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/tweet?username={member.name}&displayname={member.name}&avatar={self.avatar(member)}&comment={comment}")
        await ctx.send(file=image)

    @commands.command()
    async def stupid(self, ctx, comment, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/its-so-stupid?avatar={self.avatar(member)}&dog={comment}")
        await ctx.send(file=image)

    @commands.command()
    async def simpcard(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/simpcard?avatar={member.avatar}")
        await ctx.send(file=image)

    @commands.command()
    async def horny(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/horny?avatar={member.avatar}")
        await ctx.send(file=image)

    @commands.command()
    async def lolice(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        image = self.overlay(f"https://some-random-api.ml/canvas/lolice?avatar={member.avatar}")
        await ctx.send(file=image)


def setup(bot):
    bot.add_cog(Fun(bot))
