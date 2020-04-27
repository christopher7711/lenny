import discord
import random
from redbot.core import commands
from typing import Any
from discord.ext.commands import RoleConverter

Cog: Any = getattr(commands, "Cog", object)


class Teams(Cog):
    # Assign member to random team

    teams = [
        'Team 1',
        'Team 2',
        'Team 3']

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['team'])
    async def assign_team(self, ctx: commands.Context):

        role_conv = RoleConverter()
        roles = [await role_conv.convert(ctx, team) for team in self.teams]

        for role in roles:
            if role in ctx.author.roles:
                return
        
        random_team = random.choice(roles)
        await ctx.author.add_roles(random_team)
