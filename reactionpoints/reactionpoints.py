import discord
from redbot.core import commands
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class Reactionpoints(Cog):
    # generate number based reaction poll

    numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['punkte'])
    async def reactionpoints(self, ctx: commands.Context, fr: int=0, to: int=10):
        for num in self.numbers[fr:to+1]:
            await ctx.message.add_reaction(num)
