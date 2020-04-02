from .gulag import Gulag


def setup(bot):
    bot.add_cog(Gulag(bot))
