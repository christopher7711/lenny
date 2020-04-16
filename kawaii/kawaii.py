import discord
from redbot.core import commands
from typing import Any
import os, random
from redbot.core.data_manager import cog_data_path
from redbot.core import Config,checks

Cog: Any = getattr(commands, "Cog", object)


class Kawaii(Cog):
    # post random file in specified folder in discord channel
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=934735897643)
        default_global = {
            "kawaiipath": None
        }
        default_guild = {
            "kawaiipath": None
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command(aliases=["kawaiiii"])
    async def kawaii(self, ctx: commands.Context):
        path = await self.config.get_raw("kawaiipath")
        if path != None:
            try:
                await ctx.trigger_typing()
                file = random.choice(os.listdir(path))
                file = path + file
                pic = discord.File(file)
                await ctx.send(file=pic)
            except:
                path = str(cog_data_path(raw_name="Kawaii"))
                weeb = path + "/anime_communism"
                file = random.choice(os.listdir(weeb))
                file = weeb + file
                pic = discord.File(file)
                await ctx.send(file=pic)
        else:
            path = str(cog_data_path(raw_name="Kawaii"))
            weeb = path + "/anime_communism"
            file = random.choice(os.listdir(weeb))
            file = weeb + file
            pic = discord.File(file)
            await ctx.send(file=pic)
            
    @commands.command()
    @checks.is_owner()
    async def setkawaiipath(self, ctx, new_value):
        await self.config.set_raw("kawaiipath",value = new_value)
        await ctx.send("Path has been set")