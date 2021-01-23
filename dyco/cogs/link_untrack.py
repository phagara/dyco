import urllib.parse
import urlextract

import discord
from discord.ext import commands


class LinkUntrack(commands.Cog):
    """
    Reposts URLs with tracking query strings removed.
    """

    FORBIDDEN_QUERY_STRINGS = [
        "fbclid",
        "gclid",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
    ]

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # create/update TLD cache
        urlextract.URLExtract().update()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        urlextractor = urlextract.URLExtract()
        urls = urlextractor.find_urls(message.content)
        if not urls:
            return

        corrected_urls = []
        for url in urls:
            violated = False
            url = urllib.parse.urlparse(url)
            query = urllib.parse.parse_qs(url.query)
            for forbidden in self.FORBIDDEN_QUERY_STRINGS:
                if forbidden in query:
                    violated = True
                    del query[forbidden]
            if violated:
                url = url._replace(query=urllib.parse.urlencode(query, doseq=True))
                corrected_urls.append(urllib.parse.urlunparse(url))

        if corrected_urls:
            await message.add_reaction("\N{pile of poo}")
            await message.channel.send(
                "Links with tracking crap removed:\n\t- {}".format(
                    "\n\t- ".join(corrected_urls)
                )
            )
