import aiohttp
import discord
from bs4 import BeautifulSoup
from redbot.core import commands
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class Love(Cog):
    """Calculate the love percentage for two users!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lennylove"])
    async def love(
        self, ctx: commands.Context, lover, loved = none
    ):
        """Calculate the love percentage!"""

        if hasattr(lover, "display_name"):
            x = lover.display_name
        else:
            x = str(lover)
        if hasattr(loved, "display_name"):
            y = loved.display_name
        else:
            y = str(loved)
            
        loved = ctx.author

        url = "https://www.lovecalculator.com/love.php?name1={}&name2={}".format(
            x.replace(" ", "+"), y.replace(" ", "+")
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup_object = BeautifulSoup(await response.text(), "html.parser")
                try:
                    description = (
                        soup_object.find("div", attrs={"class": "result__score"}).get_text().strip()
                    )
                except:
                    description = "Dr. Lenny schläft gerade..."

        try:
            z = description[:2]
            z = int(z)
            if z > 50:
                emoji = "❤"
            elif z > 35:
                emoji = ":leninshrug:"
            else:
                emoji = "💔"
            title = "Dr. Lenny meint, die Liebe zwischen {} und {} beträgt:".format(x, y)
        except:
            emoji = ""
            title = "Dr. Lenny hat dir eine Nachricht geschickt."

        description = emoji + " " + description + " " + emoji
        em = discord.Embed(title=title, description=description, color=discord.Color.red())
        await ctx.send(embed=em)
