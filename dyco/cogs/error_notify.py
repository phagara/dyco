"""
Sends event error logs to bot owner in a DM.
"""
import traceback

from discord.ext import commands


class ErrorNotify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        info = await self.bot.application_info()
        await info.owner.send(
            "Event {}(*{}, **{}) failed:\n{}".format(
                event, args, kwargs, traceback.format_exc()
            )
        )


def setup(bot: commands.Bot) -> None:
    cog = ErrorNotify(bot)
    bot.add_cog(cog)
