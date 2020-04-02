import discord
from redbot.core import commands
from typing import Any
from discord.ext.commands import MemberConverter

Cog: Any = getattr(commands, "Cog", object)


class Gulag(Cog):
    # Put a user into Gulag

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gulag(self, ctx: commands.Context, name, time=10):

        gulag = '<:gulag:692252831436242994>'

        try:
            converter = MemberConverter()
            name = await converter.convert(ctx, name)
        except:
            await ctx.send(f'{name} sitzt nun im Zug nach Sibirien {gulag}')
