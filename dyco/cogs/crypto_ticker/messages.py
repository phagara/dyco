import dataclasses


@dataclasses.dataclass
class Message:
    pass


@dataclasses.dataclass
class Heartbeat(Message):
    chanId: int


@dataclasses.dataclass
class InfoV2(Message):
    serverId: str
    platform: dict


@dataclasses.dataclass
class TickerTradingSubscribeResponse(Message):
    chanId: int
    symbol: str
    pair: str


@dataclasses.dataclass
class TickerTradingUpdate(Message):
    chanId: int
    bid: float
    bid_size: float
    ask: float
    ask_size: float
    daily_change: float
    daily_change_relative: float
    last_price: float
    volume: float
    high: float
    low: float
