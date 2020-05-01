import os
import argparse
import yaml
from discord.ext import commands

from dyco.cogs import ALL_COGS


def main():
    try:
        with open(os.path.expanduser("~/.dycorc")) as conff:
            conf = yaml.safe_load(conff.read())
    except OSError:
        conf = None

    if conf is None:
        conf = {}

    if "DYCO_TOKEN" in os.environ:
        conf["token"] = os.environ["DYCO_TOKEN"]

    parser = argparse.ArgumentParser(description="Dyco the Discord bot.")
    parser.add_argument("--prefix", default=conf.get("prefix", "!"), help="bot command prefix")
    parser.add_argument("--token", default=conf.get("token"), help="bot auth token")
    parser.add_argument("--version", action="store_true", help="show version and exit")
    args = parser.parse_args()

    if args.version:
        print(VERSION)
    elif args.token is None:
        raise Exception("Bot auth token not set! Create ~/.dycorc, set DYCO_TOKEN or use --token option.")
    else:
        bot = commands.Bot("!")
        for cog in ALL_COGS:
            bot.add_cog(cog(bot))
        bot.run(args.token)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
