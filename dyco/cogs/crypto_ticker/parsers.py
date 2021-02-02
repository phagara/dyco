import typing

from .config import Config
from .messages import (
    Message,
    Heartbeat,
    InfoV2,
    TickerTradingSubscribeResponse,
    TickerTradingUpdate,
)
from .validators import (
    VALIDATOR_CONFIG,
    VALIDATOR_HEARTBEAT,
    VALIDATOR_INFO_V2,
    VALIDATOR_TICKER_TRADING_SUBSCRIBE_RESPONSE,
    VALIDATOR_TICKER_TRADING_UPDATE,
)


def parse_config(config: typing.Mapping[str, typing.Any]) -> Config:
    # .validate() raises exception if not valid
    VALIDATOR_CONFIG.validate(config)

    return Config(
        channel=config["channel"], separator=config["separator"], pairs=config["pairs"],
    )


def parse_message(
    message: typing.Union[typing.Mapping[str, typing.Any], typing.List]
) -> Message:
    if VALIDATOR_HEARTBEAT.is_valid(message):
        return Heartbeat(chanId=message[0],)
    if VALIDATOR_INFO_V2.is_valid(message):
        return InfoV2(serverId=message["serverId"], platform=message["platform"],)
    if VALIDATOR_TICKER_TRADING_SUBSCRIBE_RESPONSE.is_valid(message):
        return TickerTradingSubscribeResponse(
            chanId=message["chanId"], symbol=message["symbol"], pair=message["pair"],
        )
    if VALIDATOR_TICKER_TRADING_UPDATE.is_valid(message):
        return TickerTradingUpdate(
            chanId=message[0],
            bid=message[1][0],
            bid_size=message[1][1],
            ask=message[1][2],
            ask_size=message[1][3],
            daily_change=message[1][4],
            daily_change_relative=message[1][5],
            last_price=message[1][6],
            volume=message[1][7],
            high=message[1][8],
            low=message[1][9],
        )
    raise ValueError(f"Message does not match any known format: {message}")
