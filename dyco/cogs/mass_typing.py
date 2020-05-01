import datetime
from typing import Union

import discord
from discord.ext import commands


class MassTyping(commands.Cog):
    def __init__(self, bot: "commands.Bot"):
        self.bot = bot
        self.typing = {}

    @commands.Cog.listener()
    async def on_typing(
        self,
        channel: "discord.abc.Messageable",
        user: Union["discord.User", "discord.Member"],
        when: "datetime.datetime",
    ):
        if channel not in self.typing:
            self.typing[channel] = {}
        if user != self.bot.user:
            self.typing[channel][user] = when

        for typing_user, typing_start in self.typing[channel].copy().items():
            age = datetime.datetime.utcnow() - typing_start
            age_sec = max(age.total_seconds(), 0)
            if age_sec > 10:
                del self.typing[channel][typing_user]

        if len(self.typing[channel]) >= 3:
            await channel.trigger_typing()
