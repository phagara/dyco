import os
import logging
import pathlib
import argparse
import yaml
from discord.ext import commands


def main2():
    conf_env_vars = {
        "DYCO_PREFIX": "bot command prefix",
        "DYCO_TOKEN": "bot auth token",
        "DYCO_CONFIG": "bot config file path",
    }

    config_path_raw = os.environ.get("DYCO_CONFIG", "~/.dycorc")
    config_path = pathlib.Path(config_path_raw).expanduser()

    try:
        with open(config_path, encoding="utf-8") as conff:
            conf = yaml.safe_load(conff.read())
    except OSError:
        conf = None

    if conf is None:
        conf = {}

    version = os.environ.get("DYCO_VERSION")
    for var in conf_env_vars:
        if var in os.environ:
            conf[var[5:].lower()] = os.environ[var]

    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = "Dyco the Discord bot."
    parser.epilog = "Supported env variables:\n  {}".format(
        "\n  ".join(["{}\t{}".format(var, desc) for var, desc in conf_env_vars.items()])
    )
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    parser.add_argument(
        "--prefix", default=conf.get("prefix", "!"), help="bot command prefix"
    )
    parser.add_argument("--token", default=conf.get("token"), help="bot auth token")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if args.version:
        print(version)
    elif args.token is None:
        raise Exception(
            f"Bot auth token not set! Create {config_path_raw}, set DYCO_TOKEN or use --token option."
        )
    else:
        bot = commands.Bot(
            command_prefix=args.prefix,
            description="Dyco the Discord bot (build: {}).".format(version),
        )
        bot.load_extension(f"{__package__}.cog_manager")
        cog_manager = bot.get_cog("CogManager")
        cog_manager.conf = conf.get("cogs", {})
        bot.run(args.token)


def main():
    try:
        main2()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
