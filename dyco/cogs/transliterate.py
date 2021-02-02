"""
Transliterates to and from various language scripts.
"""
import typing
import transliterate

from discord.ext import commands


AVAIL_SCRIPTS = {
    pack.language_code: pack.language_name
    for pack in transliterate.get_available_language_packs()
}


class ScriptCode(str):
    @staticmethod
    def avail_as_str():
        return ", ".join(
            ["{} ({})".format(code, name) for code, name in AVAIL_SCRIPTS.items()]
        )

    def __new__(cls, text):
        if text in AVAIL_SCRIPTS:
            return str(text)
        raise TypeError(
            "Unknown target script code. Pick one of: {}".format(cls.avail_as_str())
        )


class Transliterate(commands.Cog):
    @commands.command()
    async def translit(self, ctx: commands.Context, target: ScriptCode, *, text: str):
        """
        Transliterates text to given script
        """
        await ctx.send(transliterate.translit(text, language_code=target))

    @commands.command()
    async def untranslit(
        self,
        ctx: commands.Context,
        source: typing.Optional[  # pylint: disable=unsubscriptable-object
            ScriptCode
        ] = None,
        *,
        text: str,
    ):
        """
        Transliterates text back to latin script
        """
        await ctx.send(
            transliterate.translit(text, language_code=source, reversed=True)
        )

    @commands.command()
    async def scriptlist(self, ctx: commands.Context):
        """
        List available language scripts
        """
        await ctx.send(
            "Available language scripts: {}".format(ScriptCode.avail_as_str())
        )


def setup(bot: commands.Bot) -> None:
    cog = Transliterate(bot)
    bot.add_cog(cog)
