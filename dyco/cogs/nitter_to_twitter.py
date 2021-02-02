"""
Rewrites nitter.net URLs to twitter.com.
"""
import urllib.parse
import urlextract

import discord
from discord.ext import commands


class NitterToTwitter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.urlextractor = urlextract.URLExtract()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        urls = self.urlextractor.find_urls(message.content)
        if not urls:
            return

        rewritten_urls = []
        for url in urls:
            url = urllib.parse.urlparse(url)
            if url.netloc == "nitter.net":
                url = url._replace(netloc="twitter.com", fragment="",)
                rewritten_urls.append(urllib.parse.urlunparse(url))

        if rewritten_urls:
            await message.channel.send(
                "Direct Twitter URLs in case Nitter is rate-limited:\n\t- {}".format(
                    "\n\t- ".join(rewritten_urls)
                )
            )


def setup(bot: commands.Bot) -> None:
    cog = NitterToTwitter(bot)
    bot.add_cog(cog)
