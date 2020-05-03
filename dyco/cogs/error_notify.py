import traceback

from discord.ext import commands


class ErrorNotify(commands.Cog):
    def __init__(self, bot: "commands.Bot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        info = await self.bot.application_info()
        await info.owner.send(
            "Event {}(*{}, **{}) failed:\n{}".format(
                event, args, kwargs, traceback.format_exc()
            )
        )
