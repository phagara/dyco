"""
Sends a DM to bot owner on reconnect.
"""
from discord.ext import commands


class ReconnectNotify(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.frist = True

    @commands.Cog.listener()
    async def on_ready(self):
        if self.frist:
            self.frist = False
        else:
            info = await self.bot.application_info()
            await info.owner.send("Dyco reconnected!")


def setup(bot: commands.Bot) -> None:
    cog = ReconnectNotify(bot)
    bot.add_cog(cog)
