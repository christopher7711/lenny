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
        # TODO: Add config so that only one list per channel exists
        # which is reposted if !speakerlist is called again

    @commands.command(aliases=['redeliste', 'rednerliste', 'rednerinnenliste'])
    async def speakerlist(self, ctx: commands.Context):
        if True:
            self.msg = await ctx.send('Bitte Warten...')
            await self.msg.pin()
            await self._refresh()
        else:
            # TODO: Repost list and delete old one if exists
            pass

    async def _refresh(self):
        say = await self._make_list()
        await self.msg.edit(content=say)
        await self.msg.clear_reactions()
        for emoji in self.emoji:
            await self.msg.add_reaction(emoji)

    async def _make_list(self):
        msg = ''
        names = [user.mention for user in self.lst]
        if not names:
            names = ['niemand']
        for i, name in enumerate(names):
            if i == 0:
                msg += '**RednerIn: **' + name + '\n'
                if len(names) < 2:
                    break
                else: msg += 'In Vorbereitung: '
            if i > 1:
                msg += ' '*31
            msg += name + '\n'
        return msg
    
    @commands.command(aliases=['hochreihen'])
    async def bump(self, ctx, speaker: discord.member, by: int=1):
        if speaker in self.lst:
            index = self.lst.index(speaker) - by
            self.lst.remove(speaker)
            self.lst.insert(index, speaker)
        await self._refresh()
    
    @commands.Cog.listener()
    async def on_react(self, reaction, user):
        
        if reaction.message.id != self.msg.id:
            return
        
        if user == self.bot.user:
            return
        
        if str(reaction.emoji) == self.emoji[0]:
            if user not in self.lst:
                self.lst.append(user)
        
        if str(reaction.emoji) == self.emoji[1]:
            if user in self.lst:
                self.lst.remove(user)
        
        if str(reaction.emoji) == self.emoji[2]:
            if self.lst:
                self.lst.pop(0)

        if str(reaction.emoji) == self.emoji[3]:
            await self.msg.delete()
            return

        await self._refresh()
