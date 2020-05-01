from discord.ext import commands


class Quit(commands.Cog):
    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        await ctx.bot.logout()
