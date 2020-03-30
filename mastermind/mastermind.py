from .game import Board, Line
from .player import Player
import discord
from redbot.core import commands
from typing import Any
from discord.ext.commands import MemberConverter

Cog: Any = getattr(commands, "Cog", object)


class Mastermind(Cog):
    # Play the game Mastermind

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mastermind(self, ctx: commands.Context, mode='guess', *args):

        def guess_check(msg):
            return len(msg.content) == 4 and all(c in colors for c in msg.content)
            
        if 'colors' in args:
            i = args.index('colors')
            colors = args[i+1]
        else:
            colors = '🔴🟠🟡🟢🔵🟣🟤⚪'

        if mode == 'auto':
            player = Player(colors)
            board = Board(colors=colors)
            await ctx.send('Die Lösung ist ||{}||'.format(''.join(board.solution)))
            for line in board.lines:
                line.fill(player.play())
                line.eval(board.solution)
                await ctx.send('Ist es {}? <:marxthink:692250502473187368>'.format(''.join(line.pegs)))
                if line.k == 4:
                    await ctx.send('GEWONNEN <:PogU:694323950448279623>')
                    return
                await ctx.send('🔸 {}   🔹 {}'.format(line.w, line.k))
                player.elim(line)
        
        if mode == 'guess':
            board = Board(colors=colors)
            await ctx.send('Die Lösung ist: ||{}||'.format(''.join(board.solution)))
            for i, line in enumerate(board.lines):
                try:
                    guess = await self.bot.wait_for('message', check=guess_check, timeout=60.0)
                except:
                    await ctx.send('zu langsam {}'.format(ctx.author.display_name))
                    return
                line.fill(guess.content)
                line.eval(board.solution)
                if line.k == 4:
                    await ctx.send('GEWONNEN <:PogU:694323950448279623>')
                    return
                await ctx.send('🔸 {}   🔹 {}'.format(line.w, line.k))

        await ctx.send('VERLOREN <:PepeHands:692256403381026817>')
