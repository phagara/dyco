"""
Continuously updates a channel topic with cryptocurrency exchange rates.
"""
from discord.ext import commands

from dyco.cog_manager import get_config
from .crypto_ticker import CryptoTicker


def setup(bot: commands.Bot) -> None:
    config = get_config(bot, "crypto_ticker")
    cog = CryptoTicker(bot, config)
    bot.add_cog(cog)
