from discord.ext import commands


class Version(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def version(self, ctx: commands.Context):
        """
        Shows the bot's version
        """
        await ctx.send(self.bot.description)
