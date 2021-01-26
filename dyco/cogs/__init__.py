from .cog_manager import CogManager
from .crypto_ticker import CryptoTicker
from .error_notify import ErrorNotify
from .latency import Latency
from .link_untrack import LinkUntrack
from .mass_typing import MassTyping
from .nitter_to_twitter import NitterToTwitter
from .quit import Quit
from .reconnect_notify import ReconnectNotify
from .status import Status
from .transliterate import Transliterate
from .uptime import Uptime
from .version import Version

ALL_COGS = [
    CogManager,
    CryptoTicker,
    ErrorNotify,
    Latency,
    LinkUntrack,
    MassTyping,
    NitterToTwitter,
    Quit,
    ReconnectNotify,
    Status,
    Transliterate,
    Uptime,
    Version,
]
