import os
import asyncio
import discord
from discord.ext import commands

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recover()

    def recover(self):
        try:
            with open('cache.txt') as cache:
                self.rrs = eval(cache.read())
        except:
            self.rrs = {}

    def update_cache(self):
        with open('cache.txt', 'w') as f:
            f.write(str(self.rrs))

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))    
    async def manualrr(self, ctx, data):
        await ctx.send('You are about to rewrite whole cache! Are you sure you want to do this?')
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            answer = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('1 წუთი ამოიწურა, ვწყვეტ ლოდინს')
            return
        else:
            if answer.content != 'yes':
                return

        try:
            self.rrs = eval(data)
        except:
            await ctx.send('ფორმატი არასწორია')
            return

        try:
            await ctx.author.send('Backup just in case...', file=discord.File('cache.txt'))
        except:
            pass

        with open('cache.txt', 'w') as cache:
            cache.write(data)

        await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def backuprr(self, ctx):
        try:
            await ctx.author.send(file=discord.File('cache.txt'))
        except:
            await ctx.send('Sending the message failed.')
        else:
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def mkrr(self, ctx, channel: discord.TextChannel, title, description, r: int, g: int, b: int):
        if not channel:
            channel = ctx.channel

        embed = discord.Embed(
            type='rich',
            title=title,
            description=description,
            color=discord.Colour.from_rgb(r, g, b)
        )
        msg = await channel.send(embed=embed)
        if ctx.guild.id in self.rrs:
            self.rrs[ctx.guild.id][msg.id] = {'channel': msg.channel.id}
        else:
            self.rrs[ctx.guild.id] = {msg.id: {'channel': msg.channel.id}}
        self.update_cache()
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def lsrr(self, ctx, msg_id: int=None):
        if msg_id:
            try:
                channel = await self.bot.fetch_channel(self.rrs[ctx.guild.id][msg_id]['channel'])
            except KeyError:
                await ctx.send('ID არასწორია')
                return

            message = await channel.fetch_message(msg_id)
            reactions = sum([r.count for r in message.reactions]) - len(message.reactions)
            embed = discord.Embed(
                type='rich',
                title=f'დეტალური ინფორმაცია `{msg_id}` -სთვის',
                description=f'რეაქციების ჯამური რაოდენობა - {reactions}',
                color=discord.Colour.green()
            )

            for reaction in message.reactions:
                role = ctx.guild.get_role(self.rrs[ctx.guild.id][msg_id][str(reaction.emoji)])
                embed.add_field(
                    name=f'{reaction.emoji} დაკავშირებულია როლთან `{role.name}`',
                    value=f'რეაქციების რაოდენობა: {reaction.count - 1 if reaction.me else reaction.count}',
                    inline=False
                )

            await ctx.send(embed=embed)
        else:
            try:
                guild_init = self.rrs[ctx.guild.id]
            except KeyError:
                await ctx.send('სერვერზე RR არ არის გააქტიურებული')
                return

            embed = discord.Embed(
                type='rich',
                title=f'Reaction Roles for `{ctx.guild.name}`',
                description=f'დეტალური ინფორმაციისთვის გამოიყენე `{self.bot.command_prefix}lsrr <id>`',
                color=discord.Colour.green()
            )

            for _id, init in guild_init.items():
                channel = await self.bot.fetch_channel(init['channel'])
                message = await channel.fetch_message(_id)
                embed.add_field(
                    name=str(_id),
                    value=message.jump_url,
                    inline=False
                )

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(int(os.environ["OWNER_ROLE_ID"]))
    async def rrinit(self, ctx, msg_id: int):
        if ctx.guild.id not in self.rrs:
            await ctx.send('სერვერზე RR არ არის გააქტიურებული')
            return
        
        if msg_id in self.rrs[ctx.guild.id]:
            try:
                channel = await self.bot.fetch_channel(self.rrs[ctx.guild.id][msg_id]['channel'])
                rr_msg = await channel.fetch_message(msg_id)
            except discord.NotFound:
                await ctx.send('მესიჯი ან ის ჩენელი სადაც მესიჯი იყო გამოგზავნილი წაშლილია, თუმცა ID-ები მაინც შენახულია')
                return
        else:
            await ctx.send('მესიჯის ID არასწორია')
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        def id_from_name(role_name):
            for role in ctx.guild.roles:
                if role.name == role_name:
                    return role.id
            return None

        helper = await ctx.send('დაიწყე ჩამოთვლა მსგავსი ფორმატით: `<emoji> <roleName>`')
        await ctx.message.delete()
        
        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                emoji, role_name = msg.content.strip().split()
            except asyncio.TimeoutError:
                await ctx.channel.send('1 წუთი ამოიწურა, ვწყვეტ ლოდინს')
                return
            except ValueError:
                if msg.content == 'done':
                    await helper.delete()
                    await msg.add_reaction('✅')
                    await msg.delete(delay=3.0)
                    return
                await ctx.send(f'ფორმატი უნდა გამოიყურებოდეს შემდეგ ნაირად: `<emoji> <roleName>`')
            else:
                role_id = id_from_name(role_name)
                if not role_id:
                    await ctx.send(f'როლის სახელი (`{role_name}`) არასწორია')
                    continue

                try:
                   await rr_msg.add_reaction(emoji)
                except discord.HTTPException:
                    if isinstance(emoji, discord.Emoji):
                        await ctx.send(f'ემოჯი (ID: `{emoji.id}`) არ არის სერვერზე დამატებული')
                    else:
                        await ctx.send(f'ემოჯის ({emoji}) ვერ ვიყენებ')
                else:
                    self.rrs[ctx.guild.id][msg_id][emoji] = role_id
                    self.update_cache()
                    await msg.delete()

    def role_for_emoji(self, emoji, guild_id, message_id):
        try:
            msg_init = self.rrs[guild_id][message_id]
        except KeyError:
            return None

        if emoji in msg_init:
            guild = self.bot.get_guild(guild_id)
            return guild.get_role(msg_init[emoji])
        return 0

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        role = self.role_for_emoji(str(payload.emoji), payload.guild_id, payload.message_id)
        if role == 0:
            channel = await self.bot.fetch_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            await msg.clear_reaction(payload.emoji)
            return
        if role:
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        role = self.role_for_emoji(str(payload.emoji), payload.guild_id, payload.message_id)
        if role and role != 0:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)


def setup(bot):
    bot.add_cog(RoleManagement(bot))
