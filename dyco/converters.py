import validators
from discord.ext import commands


class ValidURL(commands.Converter):
    def __init__(self, public: bool = False):
        self.public = public

    async def convert(self, ctx, argument):
        if not validators.url(argument, public=self.public):
            raise commands.BadArgument("Not an URL")
