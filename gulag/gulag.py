import discord
import asyncio
from redbot.core import commands
from typing import Any
from discord.ext.commands import MemberConverter, RoleConverter

Cog: Any = getattr(commands, "Cog", object)

_gulag = dict()

role_conv = RoleConverter()
member_conv = MemberConverter()

gulag_emoji = '<:gulag:692252831436242994>'
gulag_chan = '<#695361803315707904>'

class Gulag(Cog):
    # Put a user into Gulag

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gulag(self, ctx: commands.Context, name, time:float=10):

        global _gulag

        admin_role = await role_conv.convert(ctx, 'admin')
        gulag_role = await role_conv.convert(ctx, 'gulag')

        try:
            member = await member_conv.convert(ctx, name)
        except:
            if name in _gulag.keys():
                await ctx.send(f'{name.title()} ist bereits im {gulag_chan}')
            else:
                _gulag.update({name.title() : None})
                await ctx.send(f'{name.title()} sitzt nun im Zug nach Sibirien {gulag_emoji}')
            return

        if ctx.author.top_role < admin_role:
            return
        
        _gulag.update({member.mention : member.roles})
        await ctx.send('{} wurde für {} Minute{} ins {} geschickt {}'.format(
            member.mention, time, "n" if time != 1 else "", gulag_chan, gulag_emoji))
        for role in member.roles:
            await member.remove_roles(role)
        await member.add_roles(gulag_role)

        await asyncio.sleep(60 * time)

        roles = _gulag.pop(member.mention, None)
        if not roles:
            return

        await member.remove_roles(gulag_role)
        for role in roles:
            await member.add_roles(role)


    @commands.command()
    async def ungulag(self, ctx: commands.Context, name):
        
        global _gulag

        admin_role = await role_conv.convert(ctx, 'admin')
        gulag_role = await role_conv.convert(ctx, 'gulag')

        try:
            member = await member_conv.convert(ctx, name)
        except:
            if name in _gulag.keys():
                _gulag.pop(name.title(), None)
                await ctx.send(f'{name.title()} wurde aus dem Gulag entlassen')
            else:
                await ctx.send(f'{name.title()} ist nicht im {gulag_chan}')
            return

        if ctx.author.top_role < admin_role:
            return

        roles = _gulag.pop(member.mention, None)
        if not roles:
            await ctx.send(f'{member.mention} ist nicht im {gulag_chan}')
            return

        await ctx.send('{} wurde von {} aus dem {} entlassen'.format(
            member.mention, ctx.author.mention, gulag_chan))
        await member.remove_roles(gulag_role)
        for role in roles:
            await member.add_roles(role)
    
    @commands.command()
    async def whoingulag(self, ctx: commands.Context):

        if not _gulag:
            await ctx.send(f'Niemand ist im {gulag_chan} <:PepeHands:692256403381026817>')
        else:
            await ctx.send(f'Im {gulag_chan} ist: {", ".join(_gulag.keys())}')
