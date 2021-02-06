"""
Bypasses the paywall of various news sites.
"""
import aiohttp
from discord.ext import commands

from dyco.converters import ValidURL


class Unpaywall(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=5),
            raise_for_status=True
        )

    def cog_unload(self):
        self.session.close()

    @commands.command()
    async def unpaywall(self, ctx: commands.Context, url: ValidURL(public=True)):
        """
        Try to bypass the paywall of various news sites.
        """
        try:
            async with self.session.head(f"https://{url}", allow_redirects=True) as resp:
                await ctx.reply(f"{resp.url}")
        except aiohttp.ClientError as exc:
            await ctx.reply(f"Unpaywalling failed: {exc}")


def setup(bot: commands.Bot) -> None:
    cog = Unpaywall(bot)
    bot.add_cog(cog)
