import datetime
import humanize

from discord.ext import commands


class Latency(commands.Cog):
    """
    Measures the Doscord websocket latency.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def latency(self, ctx: commands.Context):
        """
        Shows the Discord websocket latency
        """
        latency = datetime.timedelta(seconds=self.bot.latency)
        await ctx.send(humanize.naturaldelta(latency, minimum_unit="milliseconds"))
