import typing

import discord
from discord.ext import commands


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def status(
        self,
        ctx: commands.Context,
        emoji: typing.Optional[discord.Emoji] = None,
        *,
        status: str
    ):
        """
        Sets the bot's status
        """
        status = discord.CustomActivity(name=status, emoji=emoji)
        await self.bot.change_presence(activity=status)
