from .reactionpoints import Reactionpoints


def setup(bot):
    bot.add_cog(Reactionpoints(bot))
