"""
Tracks the bot's uptime.
"""
import datetime
import humanize

from discord.ext import commands


class Uptime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.started_at = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.started_at = datetime.datetime.now()

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """
        Shows how long the bot has been running for
        """
        uptime = datetime.datetime.now() - self.started_at
        human_uptime = humanize.naturaldelta(-uptime)
        await ctx.send("Up {}.".format(human_uptime))


def setup(bot: commands.Bot) -> None:
    cog = Uptime(bot)
    bot.add_cog(cog)
