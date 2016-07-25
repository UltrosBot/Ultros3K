# coding=utf-8
import os

from collections import namedtuple

__author__ = "Gareth Coles"

Packages = namedtuple("Packages", ["config", "data"])


extensions = {
    "conf": Packages("ultros.storage.config.ini", "ultros.storage.data.ini"),
    "ini": Packages("ultros.storage.config.ini", "ultros.storage.data.ini"),
    "json": Packages("ultros.storage.config.json", "ultros.storage.data.json"),
    "yml": Packages("ultros.storage.config.yaml", "ultros.storage.data.yaml"),

    "properties": Packages(
        "ultros.storage.config.properties",  "ultros.storage.data.properties"
    ),
}


def get_format_from_path(path: str):
    filename = os.path.split(path)[1]

    if "." not in filename:
        # Allows one to just pass in the extension as required
        extension = filename
    else:
        extension = filename.split(".", 1)[1]

    while True:
        # Looping here for compound extensions. For example, if we have
        # file.a.b.c, then we check in order for: a.b.c, b.c, and then c

        if extension in extensions:
            return extensions[extension]

        if "." not in extension:
            break

        extension = extension.split(".", 1)[1]

    return None


def add_format(extension: str, packages: Packages):
    if extension in extensions:
        return False

    extensions[extension] = packages
    return True


def remove_format(extension: str):
    if extension not in extensions:
        return False

    del extensions[extension]
    return True
