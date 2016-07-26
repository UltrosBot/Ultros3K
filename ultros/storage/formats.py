# coding=utf-8
import os

from collections import namedtuple
from typing import Optional

__author__ = "Gareth Coles"

Packages = namedtuple("Packages", ["name", "config", "data"])

_ini_package = Packages(  # DRY
    "INI",
    "ultros.storage.config.ini",
    "ultros.storage.data.ini"
)


class Formats:
    def __init__(self):
        self._extensions = {
            "conf": _ini_package,
            "ini": _ini_package,

            "json": Packages(
                "JSON",
                "ultros.storage.config.json",
                "ultros.storage.data.json"
            ),

            "yml": Packages(
                "YAML",
                "ultros.storage.config.yaml",
                "ultros.storage.data.yaml"
            ),

            "properties": Packages(
                "Properties",
                "ultros.storage.config.properties",
                "ultros.storage.data.properties"
            ),
        }

    def get_format_from_path(self, path: str) -> Optional[Packages]:
        filename = os.path.split(path)[1]

        # We do it this way in case the plain extension was passed in
        extension = filename.split(".", 1)[-1]

        while True:
            # Looping here for compound extensions. For example, if we have
            # file.a.b.c, then we check in order for: a.b.c, b.c, and then c

            if extension in self._extensions:
                return self._extensions[extension]

            if "." not in extension:
                break

            extension = extension.split(".", 1)[1]

        return None

    def add_format(self, extension: str, packages: Packages) -> bool:
        if extension in self._extensions:
            return False

        self._extensions[extension] = packages
        return True

    def remove_format(self, extension: str) -> bool:
        if extension not in self._extensions:
            return False

        del self._extensions[extension]
        return True
