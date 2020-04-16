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
            "kawaiipath": None,
            "kawaiilist": []
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command(aliases=["kawaiiii"])
    async def kawaii(self, ctx: commands.Context):
        path = await self.config.get_raw("kawaiipath")
        list = await self.config.get_raw("kawaiilist")
        leng = len(list)
        if leng == 0:
            path = await self.config.get_raw("kawaiipath")
            if path != None:
                filelist = os.listdir(path)
                random.shuffle(filelist)
                await self.config.set_raw("kawaiilist",value = filelist)
                list = await self.config.get_raw("kawaiilist")
            else:
                path = str(cog_data_path(raw_name="Kawaii")) + "/anime_communism/"
                filelist = os.listdir(path)
                random.shuffle(filelist)
                await self.config.set_raw("kawaiilist",value = filelist)
                list = await self.config.get_raw("kawaiilist")
        leng = len(list)
        if path != None:
            try:
                await ctx.trigger_typing()
                file = list[leng - 1]
                file = path + file
                pic = discord.File(file)
                list.pop()
                await self.config.set_raw("kawaiilist",value = list)
                await ctx.send(file=pic)
            except:
                path = str(cog_data_path(raw_name="Kawaii"))
                weeb = path + "/anime_communism/"
                file = list[leng - 1]
                file = weeb + file
                pic = discord.File(file)
                list.pop()
                await self.config.set_raw("kawaiilist",value = list)
                await ctx.send(file=pic)
        else:
            path = str(cog_data_path(raw_name="Kawaii"))
            weeb = path + "/anime_communism/"
            file = list[leng - 1]
            file = weeb + file
            pic = discord.File(file)
            list.pop()
            await self.config.set_raw("kawaiilist",value = list)
            await ctx.send(file=pic)
            
    @commands.command()
    @checks.is_owner()
    async def setkawaiipath(self, ctx, new_value):
        await self.config.set_raw("kawaiipath",value = new_value)
        await ctx.send("Path has been set")

    @commands.command()
    @checks.is_owner()
    async def updatekawaii(self, ctx):
        path = await self.config.get_raw("kawaiipath")
        if path != None:
            filelist = os.listdir(path)
            random.shuffle(filelist)
            await self.config.set_raw("kawaiilist",value = filelist)
        else:
            path = str(cog_data_path(raw_name="Kawaii")) + "/anime_communism/"
            filelist = os.listdir(path)
            random.shuffle(filelist)
            await self.config.set_raw("kawaiilist",value = filelist)
        await ctx.send("File list updated")

    @commands.command()
    @checks.is_owner()
    async def showkawaii(self, ctx):
        list = await self.config.get_raw("kawaiilist")
        for i in list:
            await ctx.send(content = i)
        