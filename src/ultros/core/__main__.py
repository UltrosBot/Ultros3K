# coding=utf-8
import argparse
import logging
import os

from ultros.core.ultros import Ultros

"""
Ultros - Module runnable
"""

__author__ = "Gareth Coles"
__version__ = "0.0.1"


def start(arguments):
    logging.basicConfig(  # TODO: Proper logging
        format="%(asctime)s | %(levelname)-8s | %(name)-10s | %(message)s",
        level=logging.DEBUG if arguments.debug else logging.INFO
    )

    config_dir = os.environ.get("ULTROS_CONFIG_DIR", arguments.config)
    data_dir = os.environ.get("ULTROS_DATA_DIR", arguments.data)

    u = Ultros(config_dir, data_dir)
    u.setup()
    u.run()


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
    parser.add_argument(
        "--debug", help="Enable debug output", action="store_true"
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
