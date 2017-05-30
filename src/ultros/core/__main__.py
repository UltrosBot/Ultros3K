# coding=utf-8
import argparse
import asyncio

from ultros.core.ultros import Ultros

"""
Ultros - Module runnable
"""

__author__ = "Gareth Coles"
__version__ = "0.0.1"


def start(arguments):
    u = Ultros(arguments.config, arguments.data)
    u.start()


def init(arguments):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ultros")

    parser.add_argument(
        "--version", action="version", version="Ultros {}".format(__version__)
    )

    parser.add_argument(
        "--config", help="specify a directory containing configuration files",
        default="./config"
    )
    parser.add_argument(
        "--data", help="specify a directory to store data files",
        default="./data"
    )

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser(
        "init", help="Create a default directory structure with example files"
    )
    parser_init.set_defaults(func=init)

    parser_start = subparsers.add_parser("start", help="Start Ultros")
    parser_start.set_defaults(func=start)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()
