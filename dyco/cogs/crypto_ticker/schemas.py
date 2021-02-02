SCHEMA_CONFIG = {
    "type": "object",
    "properties": {
        "channel": {
            "type": "integer",
        },
        "pairs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "pair": {
                        "type": "string",
                    },
                    "quote_symbol": {
                        "type": "string",
                    },
                    "quote_format": {
                        "type": "string",
                    },
                    "quote_precision": {
                        "type": "integer",
                    },
                },
                "required": [
                    "pair",
                ],
            },
        },
    },
    "required": [
        "channel",
        "pairs",
    ],
}

SCHEMA_HEARTBEAT = {
    "type": "array",
    "items": [
        {
            "type": "integer",
        },
        {
            "const": "hb",
        },
    ],
}

SCHEMA_INFO_V2 = {
    "type": "object",
    "properties": {
        "event": {
            "const": "info",
        },
        "version": {
            "type": "integer",
            "const": 2,
        },
        "serverId": {
            "type": "string",
        },
        "platform": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "integer",
                },
            },
            "required": [
                "status",
            ],
        },
    },
    "required": [
        "event",
        "version",
        "serverId",
        "platform",
    ],
}

SCHEMA_TICKER_TRADING_SUBSCRIBE_RESPONSE = {
    "type": "object",
    "properties": {
        "event": {
            "const": "subscribed",
        },
        "channel": {
            "const": "ticker",
        },
        "chanId": {
            "type": "integer",
        },
        "symbol": {
            "type": "string",
        },
        "pair": {
            "type": "string",
        },
    },
    "required": [
        "event",
        "channel",
        "chanId",
        "symbol",
        "pair",
    ],
}

SCHEMA_TICKER_TRADING_UPDATE = {
    "type": "array",
    "items": [
        {
            "type": "integer",
        },  # channel_id
        {
            "type": "array",
            "items": [
                {
                    "type": "number",
                },  # bid
                {
                    "type": "number",
                },  # bid_size
                {
                    "type": "number",
                },  # ask
                {
                    "type": "number",
                },  # ask_size
                {
                    "type": "number",
                },  # daily_change
                {
                    "type": "number",
                },  # daily_change_relative
                {
                    "type": "number",
                },  # last_price
                {
                    "type": "number",
                },  # volume
                {
                    "type": "number",
                },  # high
                {
                    "type": "number",
                },  # low
            ],
        },
    ],
    "additionalItems": False,
}
