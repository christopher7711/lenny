from .speakerlist import Speakerlist


def setup(bot):
    n = Speakerlist(bot)
    bot.add_cog(n)
    bot.add_listener(n.on_react, 'on_reaction_add')
