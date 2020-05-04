import typing
import inspect

from . import ALL_COGS
from discord.ext import commands


class CogManager(commands.Cog):
    """
    Cog (bot plugin) management.
    """

    def __init__(self, bot: "commands.Bot"):
        self.bot = bot
        self.all_cogs = {
            cog.qualified_name: cog for cog in ALL_COGS if not isinstance(self, cog)
        }

    def _get_loaded_cogs(self) -> typing.Mapping[str, commands.Cog]:
        return {name: obj for name, obj in self.bot.cogs.items() if obj != self}

    def _get_unloaded_cogs(self) -> typing.Mapping[str, commands.CogMeta]:
        return {
            name: cls
            for name, cls in self.all_cogs.items()
            if name not in self._get_loaded_cogs()
        }

    @staticmethod
    def _get_cog_cls_desc(cog_cls: commands.CogMeta):
        return inspect.cleandoc(cog_cls.__doc__).splitlines()[0]

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx: "commands.Context"):
        """
        Lists/enables/disables cogs.
        """
        if ctx.invoked_subcommand is None:
            await self.cog_list(ctx)

    @cog.command()
    async def cog_list(self, ctx: "commands.Context"):
        """
        Lists all installed cogs.
        """
        await ctx.send(
            "Enabled cogs:\n\t{}\nDisabled cogs:\n\t{}".format(
                "\n\t".join(
                    [
                        "{}\t{}".format(name, cog.description)
                        for name, cog in self._get_loaded_cogs()
                    ]
                ),
                "\n\t".join(
                    [
                        "{}\t{}".format(name, self._get_cog_cls_desc(cog))
                        for name, cog in self._get_unloaded_cogs()
                    ]
                ),
            )
        )

    @cog.command()
    async def cog_enable(self, ctx: "commands.Context", cog_name: str):
        """
        Enables a cog.
        """
        if cog_name not in self.all_cogs:
            await ctx.send("No such cog.")
            return

        if cog_name in self._get_loaded_cogs():
            await ctx.send("Cog already enabled.")
            return

        try:
            self.bot.add_cog(self.all_cogs[cog_name](self.bot))
        except (TypeError, commands.CommandError):
            await ctx.send("Error enabling cog!")
            return
        await ctx.send("Cog enabled.")

    @cog.command()
    async def cog_disable(self, ctx: "commands.Context", cog_name: str):
        """
        Disables a cog.
        """
        if cog_name not in self.all_cogs:
            await ctx.send("No such cog.")
            return

        if cog_name not in self._get_unloaded_cogs():
            await ctx.send("Cog already disabled.")
            return

        self.bot.remove_cog(self.bot.get_cog(cog_name))
        await ctx.send("Cog disabled.")
