from random import choice
import discord
from redbot.core import commands
from typing import Any

from .game import Board, Line
from .player import Player

Cog: Any = getattr(commands, "Cog", object)


class Mastermind(Cog):
    # Play the game Mastermind

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mastermind(self, ctx: commands.Context, mode='guess', *args):

        emoji = {
            'PogU'              : '<:PogU:694323950448279623>',
            'marxthink'         : '<:marxthink:692250502473187368>',
            'PepeHands'         : '<:PepeHands:692256403381026817>',
            'mlthink'           : '<:mlthink:692277087003869188>',
            'communism_thonk'   : '<:communism_thonk:692264388865949737>',
            'chelaugh'          : '<:chelaugh:692250704680583169>'}
        
        correct = {
            'richtig',
            'korrerkt',
            'voi'}
        
        def thonk():
            return choice([
                emoji['marxthink'],
                emoji['mlthink'],
                emoji['communism_thonk'],
                '🤔', '', '', '', '', '', '', ''])

        def guess_check(msg):
            stop_check(msg)
            num = all(c in colors for c in msg.content)
            if default and not num:
                num = all(c in 'rgbyopnw' for c in msg.content)
            return len(msg.content) == 4 and num
        
        def tip_check(msg):
            stop_check(msg)
            if msg.content in correct:
                return True
            content = msg.content.split(' ')
            try:
                content = list(map(int, content))
            except:
                return
            num = all(c in range(5) for c in content)
            return len(content) == 2 and num
        
        def stop_check(msg):
            if 'stop' in msg.content.lower():
                raise Exception('von Spielern gestoppt')
            if '!mastermind' in msg.content:
                raise Exception('ein neues Spiel wurde gestartet')
        
        async def get_msg(kind, maxtime):
            check = {
                'tip' : tip_check,
                'guess' : guess_check}
            try:
                msg =  await self.bot.wait_for(
                    'message', check=check[kind], timeout=maxtime)
                return msg.content
            except Exception as error:
                if not error.__str__().replace(' ',''):
                    errormsg = 'Zeit abgelaufen'
                else:
                    errormsg = str(error)
                await ctx.send('Spiel wurde beendet, {}. Grund: {}'.format(
                    ctx.author.display_name, errormsg))
                return None
            
        if 'colors' in args:
            i = args.index('colors')
            colors = args[i+1]
            default = False
        else:
            colors = '🔴🟢🔵🟡🟠🟣🟤⚪'
            default = True
        
        if 'time' in args:
            i = args.index('time')
            maxtime = float(args[i+1])
        else:
            maxtime = 100.0
        
        hide = True if 'hide' in args else False

        if mode == 'auto':
            player = Player(colors)
            board = Board(colors=colors)
            if not hide:
                await ctx.send('Die Lösung ist ||{}||'.format(
                    ''.join(board.solution)))
            for line in board.lines:
                line.fill(await player.play())
                line.eval(board.solution)
                await ctx.send('Ist es {}? {}'.format(
                    ''.join(line.pegs), thonk()))
                if line.k == 4:
                    await ctx.send('GEWONNEN {}'.format(emoji['PogU']))
                    return
                await ctx.send('🔸 {}   🔹 {}'.format(line.w, line.k))
                player.elim(line)

        elif mode == 'lenny':
            player = Player(colors)
            line = Line()
            while True:
                try:
                    code = await player.play()
                except IndexError:
                    await ctx.send(
                        'Kann nicht sein. Ich glaub, du hast dich vertan. {}'.format(
                            emoji['chelaugh']))
                    return
                line.fill(code)
                await ctx.send('Ist es {}? {}'.format(
                    ''.join(line.pegs), thonk()))
                tip = await get_msg('tip', maxtime)
                if tip == None:
                    return
                elif tip[2] == '4' or tip in correct:
                    await ctx.send('GEWONNEN {}'.format(emoji['PogU']))
                    return
                else:
                    tip = tip.split(' ')
                line.assist(*tip)
                player.elim(line)

        elif mode == 'guess':
            board = Board(colors=colors)
            if not hide:
                await ctx.send('Die Lösung ist ||{}||'.format(
                    ''.join(board.solution)))
            for i, line in enumerate(board.lines):
                guess = await get_msg('guess', maxtime)
                if guess == None:
                    return
                if default:
                    for letter, color in zip('rgbyopnw', colors):
                        guess = guess.replace(letter, color)
                line.fill(guess)
                line.eval(board.solution)
                if line.k == 4:
                    await ctx.send('GEWONNEN {}'.format(emoji['PogU']))
                    return
                await ctx.send('🔸 {}   🔹 {}'.format(line.w, line.k))
            await ctx.send('VERLOREN {}'.format(emoji['PepeHands']))

        else:
            return
