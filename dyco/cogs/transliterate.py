import typing
import transliterate

from discord.ext import commands


_AVAIL_SCRIPTS = {
    pack.language_code: pack.language_name
    for pack in transliterate.get_available_language_packs()
}


class _ScriptCode(str):
    @staticmethod
    def avail_as_str():
        return ", ".join(
            ["{} ({})".format(code, name) for code, name in _AVAIL_SCRIPTS.items()]
        )

    def __new__(cls, text):
        if text in _AVAIL_SCRIPTS:
            return super().__new__(text)
        raise ValueError(
            "Unknown target script code. Pick one of: {}".format(cls.avail_as_str())
        )


class Transliterate(commands.Cog):
    @commands.command()
    async def translit(
        self, ctx: "commands.Context", target: _ScriptCode, *, text: str
    ):
        """
        Transliterates text to given script
        """
        await ctx.send(transliterate.translit(text, language_code=target))

    @commands.command()
    async def untranslit(
        self,
        ctx: "commands.Context",
        source: typing.Optional[_ScriptCode] = None,
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
    async def scriptlist(self, ctx: "commands.Context"):
        """
        List available language scripts
        """
        await ctx.send(
            "Available language scripts: {}".format(_ScriptCode.avail_as_str())
        )
