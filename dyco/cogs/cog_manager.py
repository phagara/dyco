import typing
import inspect

import tabulate
from discord.ext import commands


class CogManager(commands.Cog):
    """
    Cog (bot plugin) management.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.unloaded_cogs = {}

    @property
    def loaded_cogs(self) -> typing.Mapping[str, commands.Cog]:
        return {name: obj for name, obj in self.bot.cogs.items() if obj != self}

    @property
    def all_cogs(self) -> typing.Mapping[str, commands.Cog]:
        return self.loaded_cogs | self.unloaded_cogs

    @staticmethod
    def _shortdesc(cog):
        cleaned = inspect.cleandoc(cog.description)
        lines = cleaned.splitlines()
        if "" in lines:
            lines = lines[: lines.index("")]
        return " ".join(lines)

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx: commands.Context):
        """
        Lists/enables/disables cogs
        """
        if ctx.invoked_subcommand is None:
            await self.list(ctx)

    @cog.command()
    async def list(self, ctx: commands.Context):
        """
        Lists all installed cogs
        """
        cols = ("Enabled", "Name", "Description")
        rows = (
            (name in self.loaded_cogs, name, self._shortdesc(cog))
            for name, cog in self.all_cogs.items()
        )
        table = tabulate.tabulate(rows, headers=cols)
        await ctx.send(f"```{table}```")

    @cog.command()
    async def enable(self, ctx: commands.Context, cog_name: str):
        """
        Enables a cog
        """
        if cog_name in self.loaded_cogs:
            await ctx.send("Cog already enabled.")
            return

        if cog_name not in self.unloaded_cogs:
            await ctx.send("No such cog.")
            return

        cog = self.unloaded_cogs.pop(cog_name)
        try:
            self.bot.add_cog(cog)
        except (TypeError, commands.CommandError):
            await ctx.send("Error enabling cog!")
            self.unloaded_cogs[cog_name] = cog
            return
        await ctx.send("Cog enabled.")

    @cog.command()
    async def disable(self, ctx: commands.Context, cog_name: str):
        """
        Disables a cog
        """
        if cog_name in self.unloaded_cogs:
            await ctx.send("Cog already disabled.")
            return

        if cog_name not in self.loaded_cogs:
            await ctx.send("No such cog.")
            return

        self.unloaded_cogs[cog_name] = self.bot.get_cog(cog_name)
        self.bot.remove_cog(cog_name)
        await ctx.send("Cog disabled.")
