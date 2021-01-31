import typing
import logging
import time
import json
import websockets
import humanize
import discord
from discord.ext import tasks, commands


class CryptoTicker(commands.Cog):
    """
    Continuously updates a channel topic with cryptocurrency exchange rates.
    """

    WS_API_KWARGS = {
        "uri": "wss://api-pub.bitfinex.com/ws/2",
    }
    CHANNEL_ID = 381087402741202945  # TODO: make configurable
    TOPIC_EDIT_DELAY = 600

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._channel: typing.Optional[
            discord.TextChannel
        ] = None  # pylint: disable=unsubscriptable-object
        self._sub: int = 0
        self._last_updated_at: int = 0
        self.subscribe.add_exception_type(  # pylint: disable=no-member
            websockets.exceptions.ConnectionClosedError
        )
        self.subscribe.start()  # pylint: disable=no-member

    @property
    def channel(self):
        if self._channel is None:
            self._channel = self.bot.get_channel(self.CHANNEL_ID)
        return self._channel

    def cog_unload(self):
        self.subscribe.cancel()  # pylint: disable=no-member

    @tasks.loop()
    async def subscribe(self):
        async with websockets.connect(**self.WS_API_KWARGS) as wss:
            await wss.send(
                json.dumps(
                    {"event": "subscribe", "channel": "ticker", "symbol": "tBTCUSD"}
                )
            )
            async for message in wss:
                await self.handle(json.loads(message))

    @subscribe.before_loop
    async def before_subscribe(self):
        await self.bot.wait_until_ready()

    async def handle(self, message: typing.Any):
        if isinstance(message, dict) and "chanId" in message:
            self._sub = message["chanId"]
        elif (
            isinstance(message, list) and message[0] == self._sub and message[1] != "hb"
        ):
            data = message[1]
            (
                bid,
                bid_size,
                ask,
                ask_size,
                daily_change,
                daily_change_relative,
                last_price,
                volume,
                high,
                low,
            ) = data[:10]

            if daily_change_relative >= 0.05:
                emoji = "\N{LAST QUARTER MOON WITH FACE}"
            elif daily_change_relative >= 0.02:
                emoji = "\N{ROCKET}"
            elif daily_change_relative >= 0.005:
                emoji = "\N{CHART WITH UPWARDS TREND}"
            elif daily_change_relative > -0.005:
                emoji = "\N{PINCHING HAND}"
            elif daily_change_relative > -0.02:
                emoji = "\N{CHART WITH DOWNWARDS TREND}"
            elif daily_change_relative > -0.05:
                emoji = "\N{COMET}"
            else:
                emoji = "\N{COLLISION SYMBOL}"

            if time.time() > self._last_updated_at + self.TOPIC_EDIT_DELAY:
                self._last_updated_at = time.time()
                await self.channel.edit(
                    topic=f"{emoji} ${humanize.intcomma(int(last_price))} [{daily_change_relative*100:+.2f}%]"
                )
