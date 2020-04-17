import discord
from redbot.core import commands
from typing import Any
import os, random
from redbot.core.data_manager import cog_data_path
from redbot.core import Config, checks

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
            "kawaiipath": None,
            "kawaiilist": []
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command(aliases=["kawaiiii"])
    async def kawaii(self, ctx: commands.Context):
        path = await self.config.get_raw("kawaiipath")
        klst = await self.config.get_raw("kawaiilist")

        if path is None:
            path = os.path.join(cog_data_path(raw_name="kawaii"), "anime_communism")
        
        if not klst:
            filelist = os.listdir(path)
            random.shuffle(filelist)
            await self.config.set_raw("kawaiilist", value=filelist)
            klst = await self.config.get_raw("kawaiilist")

        await ctx.trigger_typing()
        file = path + klst.pop()
        pic = discord.File(file)
        await self.config.set_raw("kawaiilist", value=klst)
        await ctx.send(file=pic)
            
    @commands.command()
    @checks.is_owner()
    async def setkawaiipath(self, ctx, new_value):
        await self.config.set_raw("kawaiipath", value=new_value)
        await ctx.send("Path has been set")

    @commands.command()
    @checks.is_owner()
    async def updatekawaii(self, ctx):
        path = await self.config.get_raw("kawaiipath")
        if path is None:
            path = os.path.join(cog_data_path(raw_name="kawaii"), "anime_communism")
        filelist = os.listdir(path)
        random.shuffle(filelist)
        await self.config.set_raw("kawaiilist", value=filelist)
        await ctx.send("File list updated")

    @commands.command()
    @checks.is_owner()
    async def showkawaii(self, ctx):
        klst = await self.config.get_raw("kawaiilist")
        for file in klst:
            await ctx.send(content=file)
        