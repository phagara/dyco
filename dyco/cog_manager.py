import typing
import inspect
import logging
import pathlib
import pkgutil
import importlib

import tabulate
from discord.ext import commands


def get_config(bot: commands.Bot, cog: str) -> typing.Mapping[str, typing.Any]:
    cog_manager = bot.get_cog("CogManager")
    return cog_manager.conf.get(cog, {})


class CogManager(commands.Cog):
    """
    Cog (bot plugin) management.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._conf: typing.Optional[typing.Mapping[str, any]] = None
        self._cogs_dir = pathlib.Path(__package__).joinpath("cogs")

    @property
    def conf(self) -> typing.Optional[typing.Mapping[str, any]]:
        return self._conf

    @conf.setter
    def conf(self, value: typing.Mapping[str, any]) -> None:
        if self._conf is not None:
            raise ValueError("Configuration was already loaded.")
        self._conf = dict(value)

        logging.info("Loading enabled cogs...")
        for cog, conf in self._conf.items():
            try:
                self.bot.load_extension(f"dyco.cogs.{cog}")
            except commands.ExtensionError:
                logging.error("Failed to load cog `%s`", cog, exc_info=True)
                continue
            logging.info("Loaded cog `%s`", cog)

    @property
    def all_cogs(self) -> typing.List[str]:
        return [mod_name for _, mod_name, _ in pkgutil.iter_modules([self._cogs_dir])]

    def is_enabled(self, cog: str) -> bool:
        return f"dyco.cogs.{cog}" in self.bot.extensions

    def _shortdesc(self, cog: str) -> str:
        if cog not in self.bot.extensions:
            importlib.invalidate_caches()
            cog_module = importlib.import_module(
                f"{__package__}.cogs.{cog}", package=__package__
            )
        else:
            cog_module = self.bot.extensions[cog]

        doc = inspect.getdoc(cog_module)

        if cog not in self.bot.extensions:
            del cog_module

        if doc is None:
            return "<None>"

        lines = doc.splitlines()
        if "" in lines:
            lines = lines[: lines.index("")]
        return " ".join(lines)

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx: commands.Context) -> None:
        """
        Lists/enables/disables cogs
        """
        if ctx.invoked_subcommand is None:
            await self.list(ctx)

    @cog.command()
    async def list(self, ctx: commands.Context) -> None:
        """
        Lists all installed cogs
        """
        cols = ("Enabled", "Name", "Description")
        rows = (
            (self.is_enabled(cog), cog, self._shortdesc(cog)) for cog in self.all_cogs
        )
        table = tabulate.tabulate(rows, headers=cols)
        await ctx.send(f"```{table}```")

    @cog.command()
    async def enable(self, ctx: commands.Context, cog_name: str) -> None:
        """
        Enables a cog
        """
        try:
            self.bot.load_extension(f"{__package__}.cogs.{cog_name}")
        except commands.ExtensionError as exc:
            await ctx.send(f"Failed to enable cog: {exc}")
            return

        await ctx.send("Cog enabled.")

    @cog.command()
    async def disable(self, ctx: commands.Context, cog_name: str) -> None:
        """
        Disables a cog
        """
        try:
            self.bot.unload_extension(f"{__package__}.cogs.{cog_name}")
        except commands.ExtensionError as exc:
            await ctx.send(f"Failed to disable cog: {exc}")
            return

        await ctx.send("Cog disabled.")

    @cog.command()
    async def reload(self, ctx: commands.Context, cog_name: str) -> None:
        """
        Reloads a cog
        """
        try:
            self.bot.reload_extension(f"{__package__}.cogs.{cog_name}")
        except commands.ExtensionError as exc:
            await ctx.send(f"Failed to reload cog: {exc}")
            return

        await ctx.send("Cog reloaded.")


def setup(bot: commands.Bot) -> None:
    logging.info("Loading cog_manager extension.")
    cog_manager = CogManager(bot)
    bot.add_cog(cog_manager)


def teardown(bot: commands.Bot) -> None:
    logging.info("Unloading cog_manager extension, will unload all cogs...")
    cog_manager = bot.get_cog(CogManager.__name__)
    for cog in cog_manager.all_cogs:
        try:
            bot.unload_extension(cog)
        except commands.ExtensionError:
            logging.error("Failed to unload cog %s", cog, exc_info=True)
            continue
        logging.info("Unloaded cog %s", cog)
