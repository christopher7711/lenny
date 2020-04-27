import discord
from redbot.core import commands
from typing import Any
from discord.ext.commands import MemberConverter

Cog: Any = getattr(commands, "Cog", object)


class Speakerlist(Cog):
    # Automatic keeping of speaker list

    emoji = '⤴⤵⏩⏸'

    def __init__(self, bot):
        self.bot = bot
        self.msg = None
        self.lst = list()

    @commands.command(aliases=['redeliste', 'rednerliste', 'rednerinnenliste'])
    async def speakerlist(self, ctx: commands.Context):
        self.msg = await ctx.send('Bitte Warten...')
        await self.msg.pin()
        await self._refresh()

    async def _refresh(self):
        say = await self._make_list()
        await self.msg.edit(content=say)
        await self.msg.clear_reactions()
        for emoji in self.emoji:
            await self.msg.add_reaction(emoji)

    async def _make_list(self):
        msg = '**RednerInnenliste:**\n'
        filler = 3 - len(self.lst)
        names = [user.mention for user in self.lst]
        names.extend(['(leer)']*filler)
        for i, name in enumerate(names):
            msg += f'    **{str(i+1)}.** ' + name + '\n'
        return msg
    
    @commands.Cog.listener()
    async def on_react(self, reaction, user):
        
        if reaction.message.id != self.msg.id:
            return
        
        if user == self.bot.user:
            return
        
        if str(reaction.emoji) == self.emoji[0]:
            if user not in self.lst:
                self.lst.append(user)
            else:
                pass
        
        if str(reaction.emoji) == self.emoji[1]:
            try:
                self.lst.remove(user)
            except ValueError:
                pass
        
        if str(reaction.emoji) == self.emoji[2]:
            try:
                self.lst.pop(0)
            except IndexError:
                pass

        if str(reaction.emoji) == self.emoji[3]:
            await self.msg.delete()
            return

        await self._refresh()
