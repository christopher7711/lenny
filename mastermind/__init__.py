from .mastermind import Mastermind


def setup(bot):
    bot.add_cog(Mastermind(bot))
