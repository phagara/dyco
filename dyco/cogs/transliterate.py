import typing
import transliterate

from discord.ext import commands


class Transliterate(commands.Cog):
    AVAIL_SCRIPTS = {
        pack.language_code: pack.language_name
        for pack in transliterate.get_available_language_packs()
    }

    async def _validate_script_code(self, ctx: "commands.Context", code: str):
        if code is not None and code not in self.AVAIL_SCRIPTS:
            await ctx.send(
                "Unknown target script code. Pick one of: {}".format(
                    ", ".join(
                        [
                            "{} ({})".format(code, name)
                            for code, name in self.AVAIL_SCRIPTS.items()
                        ]
                    )
                )
            )
            raise ValueError("unknown script code")

    @commands.command()
    async def translit(self, ctx: "commands.Context", target: str, text: str):
        """
        Transliterates text to given script
        """
        try:
            await self._validate_script_code(ctx, target)
        except ValueError:
            return
        res = transliterate.translit(text, language_code=target)
        await ctx.send(res)

    @commands.command()
    async def untranslit(
        self,
        ctx: "commands.Context",
        source: typing.Optional[str] = None,
        *,
        text: str,
    ):
        """
        Transliterates text back to latin script
        """
        try:
            await self._validate_script_code(ctx, source)
        except ValueError:
            return
        res = transliterate.translit(text, language_code=source, reversed=True)
        await ctx.send(res)
