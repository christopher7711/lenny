import discord
from redbot.core import commands
from typing import Any
from discord.ext.commands import MemberConverter

Cog: Any = getattr(commands, "Cog", object)


class Love(Cog):
    # Calculate the love percentage for two users

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lennylove"])
    async def love(self, ctx: commands.Context, name1, name2=None):
        
        # Convert ID to Member if possible
        try:
            converter = MemberConverter()
            name1 = await converter.convert(ctx, name1)
            name1 = name1.display_name
        except:
            pass

        if not name2:
            name2 = name1
            name1 = ctx.author.display_name
        else:
            try:
                converter = MemberConverter()
                name2 = await converter.convert(ctx, name2)
                name2 = name2.display_name
            except:
                pass

        # Check if lenny is involved
        if name1.lower() == "lenny" or name2.lower() == "lenny":
            lenny = True
        else:
            lenny = False

        # Generate love%
        num1 = sum([ord(x)**1.249 for x in name1.lower()])
        num2 = sum([ord(x)**1.249 for x in name2.lower()])
        z = (abs(num1 - num2) - 1) % 101

        # Add lenny specific bonus and choose emoji
        if lenny:
            z += (100-z)//2
        if z > 70:
            emoji = "❤"
            if lenny:
                emoji = "😻"
        elif z < 30:
            emoji = "💔"
        else:
            emoji = ""

        # Put message together
        title = "Dr. Lenny meint, die Liebe zwischen {} und {} beträgt:".format(name1, name2)
        description = emoji + " " + str(round(z)) + "% " + emoji
        em = discord.Embed(title=title, description=description, color=discord.Color.red())
        await ctx.send(embed=em)
