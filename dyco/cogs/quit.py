from discord.ext import commands


class Quit(commands.Cog):
    def __init__(self, bot: 'commands.Bot'):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        info = await self.bot.application_info()
        await info.owner.send('Dyco (re)started!')

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        await ctx.send('Shutting down...')
        await ctx.bot.logout()
