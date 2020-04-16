import discord
from redbot.core import commands
from typing import Any
import os, random
from redbot.core import Config,checks

Cog: Any = getattr(commands, "Cog", object)


class Kawaii(Cog):
    # post random file in specified folder in discord channel

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=934735897643)
        default_global = {
            "kawaiipath": "None"
        }
        default_guild = {
            "kawaiipath": "None"
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command(aliases=["kawaiiii"])
    async def kawaii(self, ctx: commands.Context):
        path = await self.config.guild(ctx.guild).kawaiipath()
        if path != "None":
            try:
                await ctx.trigger_typing()
                file = random.choice(os.listdir(path))
                file = path + file
                pic = discord.File(file)
                await ctx.send(file=pic)
            except:
                await ctx.send("Error couldnt get file check path [p]setkawaiipath")
        else:
            await ctx.send("Path not set set it with [p]setkawaiipath")
            
    @commands.command()
    @checks.is_owner()
    async def setkawaiipath(self, ctx, new_value):
        await self.config.guild(ctx.guild).kawaiipath.set(new_value)
        await ctx.send("Path has been set")