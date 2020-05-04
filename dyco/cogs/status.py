import typing
import logging

import discord
from discord.ext import commands


class Status(commands.Cog):
    """
    Bot activity status manager.

    Only playing, listening and streaming activities are supported for bots.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def status(self, ctx: commands.Context):
        """
        Set/unset bot's activity status
        """
        if ctx.invoked_subcommand is None:
            await self.get(ctx)

    @status.command()
    async def playing(self, ctx: commands.Context, *, what: str):
        """
        Sets activity to "Playing <what>"
        """
        await self.bot.change_presence(activity=discord.Game(name=what))

    @status.command()
    async def listening(self, ctx: commands.Context, *, what: str):
        """
        Sets activity to "Listening to <what>"
        """
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=what)
        )

    @status.command()
    async def streaming(self, ctx: commands.Context, *, what: str):
        """
        Sets activity to "Streaming <what>"
        """
        await self.bot.change_presence(
            activity=discord.Streaming(
                name=what, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        )

    @status.command()
    async def unset(self, ctx: commands.Context):
        """
        Unset the activity status of the bot
        """
        await self.bot.change_presence(activity=None)
