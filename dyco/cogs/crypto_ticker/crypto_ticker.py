import typing
import logging
import asyncio
import json
import functools
import websockets
import humanize
import discord
from discord.ext import tasks, commands

from .messages import (
    TickerTradingSubscribeResponse,
    TickerTradingUpdate,
)
from .parsers import parse_config, parse_message


class CryptoTicker(commands.Cog):

    WS_API_KWARGS = {
        "uri": "wss://api-pub.bitfinex.com/ws/2",
    }

    def __init__(self, bot: commands.Bot, conf: typing.Mapping[str, typing.Any]):
        self.bot = bot
        self.conf = parse_config(conf)

        self.channel_id: int = self.conf.channel
        self.tickers: typing.MutableMapping[
            str, typing.Optional[TickerTradingUpdate]
        ] = {pair: None for pair in self.conf.pairs_dict}
        self.subscriptions: typing.MutableMapping[int, str] = {}

        self.all_tickers_ready = asyncio.Event()

        self.subscribe.add_exception_type(  # pylint: disable=no-member
            websockets.exceptions.ConnectionClosedError
        )
        self.subscribe.start()  # pylint: disable=no-member
        self.topic_updater.start()  # pylint: disable=no-member

    @functools.cached_property
    def channel(self) -> discord.TextChannel:
        return self.bot.get_channel(self.channel_id)

    def cog_unload(self):
        self.subscribe.cancel()  # pylint: disable=no-member
        self.topic_updater.cancel()  # pylint: disable=no-member

    @tasks.loop()
    async def subscribe(self):
        async with websockets.connect(**self.WS_API_KWARGS) as wss:
            for pair in self.conf.pairs_dict:
                symbol = f"t{pair}"
                await wss.send(
                    json.dumps(
                        {"event": "subscribe", "channel": "ticker", "symbol": symbol}
                    )
                )
            async for message in wss:
                await self.handle(json.loads(message))

    @subscribe.before_loop
    async def before_subscribe(self):
        await self.bot.wait_until_ready()

    async def handle(self, message: typing.Any):
        try:
            message = parse_message(message)
        except ValueError:
            logging.warning("Ignoring unknown message type: %s", message)

        if isinstance(message, TickerTradingSubscribeResponse):
            self.subscriptions[message.chanId] = message.pair
            return

        if isinstance(message, TickerTradingUpdate):
            pair = self.subscriptions[message.chanId]
            self.tickers[pair] = message

            if not self.all_tickers_ready.is_set():
                if None not in self.tickers.values():
                    self.all_tickers_ready.set()

            return

    def format_ticker(self, pair, ticker: TickerTradingUpdate) -> str:
        pair_conf = self.conf.pairs_dict[pair]
        pair = pair_conf["pair"]
        prefix = pair_conf.get("prefix", f"{pair}: ")
        quote_symbol = pair_conf.get("quote_symbol", "$")
        quote_format = pair_conf.get("quote_format", "{quote_symbol}{quote_rate}")

        rate = humanize.intcomma(ticker.last_price, pair_conf.get("precision", 2))
        change_pct = ticker.daily_change_relative * 100
        quote = quote_format.replace("{quote_symbol}", quote_symbol).replace(
            "{quote_rate}", rate
        )

        return f"{prefix}{quote} [{change_pct:+.2f}%]"

    @property
    def topic(self):
        return self.conf.separator.join(
            [self.format_ticker(pair, ticker) for pair, ticker in self.tickers.items()]
        )

    @tasks.loop(minutes=10)
    async def topic_updater(self):
        await self.channel.edit(topic=self.topic)

    @topic_updater.before_loop
    async def before_topic_updates(self):
        await self.bot.wait_until_ready()
        await self.all_tickers_ready.wait()
