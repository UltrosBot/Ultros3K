# coding=utf-8
import argparse
import logging
import os
import shutil
import zipfile

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


def get_bool(prompt: str, arguments, *, default=True):
    if hasattr(arguments, "force") and arguments.force:
        return default

    data = input("> {} ".format(prompt)).strip()

    if not data:
        return default

    if data.lower() in ["y", "yes"]:
        return True
    if data.lower() in ["n", "no"]:
        return False

    print("Unknown answer: {}".format(data))
    return get_bool(prompt, arguments, default=default)


def init(arguments):
    config_dir = os.environ.get("ULTROS_CONFIG_DIR", arguments.config)
    data_dir = os.environ.get("ULTROS_DATA_DIR", arguments.data)

    print("Config dir: {}".format(config_dir))
    print("Data dir: {}".format(data_dir))
    print()

    if not get_bool("Are these paths okay? [Y/n]", arguments):
        exit(0)

    if os.path.exists(config_dir):
        overwrite = get_bool("Config directory '{}' exists - overwrite? [Y/n]".format(config_dir), arguments)

        if not overwrite:
            print("Not overwriting config directory.")
            exit(0)

        shutil.rmtree(config_dir)

    os.makedirs(config_dir, exist_ok=True)

    if not os.path.exists(data_dir):
        print("Created data directory '{}'".format(data_dir))
        os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(os.path.dirname(__file__), "../../config.zip")

    zip = zipfile.ZipFile(file_path, "r")
    zip.extractall(config_dir)
    zip.close()

    print("Created config directory '{}' with default files".format(config_dir))


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

    parser_init.add_argument(
        "--force", help="Do not prompt for decisions - overwrite everything. This is intended for unattended setups.",
        action="store_true"
    )

    parser_init.set_defaults(func=init)

    parser_start = subparsers.add_parser("start", help="Start Ultros")
    parser_start.set_defaults(func=start)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()
