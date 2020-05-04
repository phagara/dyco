import typing

from discord.ext import commands


class CogManager(commands.Cog):
    """
    Cog (bot plugin) management.
    """

    def __init__(self, bot: "commands.Bot"):
        self.bot = bot
        self.unloaded_cogs = {}

    @property
    def loaded_cogs(self) -> typing.Mapping[str, commands.Cog]:
        return {name: obj for name, obj in self.bot.cogs.items() if obj != self}

    @commands.group()
    @commands.is_owner()
    async def cog(self, ctx: "commands.Context"):
        """
        Lists/enables/disables cogs.
        """
        if ctx.invoked_subcommand is None:
            await self.list(ctx)

    @cog.command()
    async def list(self, ctx: "commands.Context"):
        """
        Lists all installed cogs.
        """
        await ctx.send(
            "Enabled cogs:\n\t{}\nDisabled cogs:\n\t{}".format(
                "\n\t".join(
                    [
                        "{}\t{}".format(name, cog.description)
                        for name, cog in self.loaded_cogs
                    ]
                ),
                "\n\t".join(
                    [
                        "{}\t{}".format(name, cog.description)
                        for name, cog in self.unloaded_cogs
                    ]
                ),
            )
        )

    @cog.command()
    async def enable(self, ctx: "commands.Context", cog_name: str):
        """
        Enables a cog.
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
    async def disable(self, ctx: "commands.Context", cog_name: str):
        """
        Disables a cog.
        """
        if cog_name in self.unloaded_cogs:
            await ctx.send("Cog already disabled.")
            return

        if cog_name not in self.loaded_cogs:
            await ctx.send("No such cog.")
            return

        cog = self.bot.get_cog(cog_name)
        self.bot.remove_cog(cog)
        self.unloaded_cogs[cog_name] = cog
        await ctx.send("Cog disabled.")
