# coding=utf-8

"""
Definitions for storage formats and what they support

This may be acted upon by plugins that wish to add their own formats.
"""

import os

from collections import namedtuple
from typing import Optional

__author__ = "Gareth Coles"

Packages = namedtuple("Packages", ("name", "config", "data"))

_ini_package = Packages(  # DRY
    "INI",
    "ultros.core.storage.config.ini",
    "ultros.core.storage.data.ini"
)

# Constants for use in other packages that want to specify a format explicitly

BIN = "bin"
CONF = "conf"
INI = "ini"
JSON = "json"
PYTHON = "py"
TOML = "toml"
TXT = "txt"
YML = "yml"
YML_ROUNDTRIP = "yml-roundtrip"


class FileFormats:
    """
    Contains information about what storage formats are supported and
    where to look for a class that implements that storage format in the
    form of a class that overrides one of the base classes. This is for
    file-based storage only.

    Essentially, each file extension is associated with a Packages namedtuple,
    containing the following information:

    * **name** (str) - The friendly name of the format
    * **config** (str or None) - Module containing the config implementation
    * **data** (str or None) - Module containing the data implementation

    These namedtuples are created as follows.

    >>> x = Packages(
    ...     "INI",
    ...     "ultros.core.storage.config.ini",
    ...     "ultros.core.storage.data.ini"
    ... )
    >>>

    When a file is loaded that matches one of the formats, the storage
    manager will load the module and scan it for the first class that
    implements StorageBase. That class is then instantiated and used as the
    storage object.

    The following formats are supported out of the box:

    +----------------+---------------------------+---------------+
    | Extension      | Format                    | Storage types |
    +================+===========================+===============+
    | .bin           | Direct-access binary file | Data only     |
    +----------------+---------------------------+---------------+
    | .conf          | INI                       | Config & Data |
    +----------------+---------------------------+---------------+
    | .ini           | INI                       | Config & Data |
    +----------------+---------------------------+---------------+
    | .json          | JSON                      | Config & Data |
    +----------------+---------------------------+---------------+
    | .py            | Python                    | Config only   |
    +----------------+---------------------------+---------------+
    | .toml          | TOML                      | Config & Data |
    +----------------+---------------------------+---------------+
    | .txt           | Direct-access text file   | Data only     |
    +----------------+---------------------------+---------------+
    | .yml           | YAML                      | Config & Data |
    +----------------+---------------------------+---------------+
    | .yml-roundtrip | YAML (round-trip parser)  | Config only   |
    +----------------+---------------------------+---------------+
    """

    def __init__(self):
        self._extensions = {
            BIN: Packages(
                "Binary File",
                None,
                "ultros.core.storage.data.binary"
            ),

            CONF: _ini_package,
            INI: _ini_package,

            JSON: Packages(
                "JSON",
                "ultros.core.storage.config.json",
                "ultros.core.storage.data.json"
            ),

            PYTHON: Packages(
                "Python",
                "ultros.core.storage.config.python",
                None
            ),

            TOML: Packages(
                "TOML",
                "ultros.core.storage.config.toml",
                "ultros.core.storage.data.toml"
            ),

            TXT: Packages(
                "Text File",
                None,
                "ultros.core.storage.data.text"
            ),

            YML: Packages(
                "YAML",
                "ultros.core.storage.config.yaml",
                "ultros.core.storage.data.yaml"
            ),

            YML_ROUNDTRIP: Packages(
                "YAML (Round-trip)",
                "ultros.core.storage.config.yaml_roundtrip",
                None
            ),
        }

    def get_format_from_path(self, path: str) -> Optional[Packages]:
        """
        Attempt to guess the format for a file, given its path, returning
        it if found.

        :param path: The path to the file. Doesn't have to be a real path.
        :return: A Package representing the file format, or None if not found.
        """

        filename = os.path.split(path)[1]

        # We do it this way in case the plain extension was passed in
        extension = filename.split(".", 1)[-1].lower()

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
        """
        Register a supported format, if the extension isn't already handled.

        :param extension: The extension to register for
        :param packages: A Packages object representing your format
        :return: False if the extension was already registered, otherwise True
        """
        if extension in self._extensions:
            return False

        self._extensions[extension] = packages
        return True

    def remove_format(self, extension: str) -> bool:
        """
        Remove an already-registered format by extension, if it exists.

        :param extension: The extension to remove
        :return: False if the extension isn't registered, True otherwise
        """

        if extension not in self._extensions:
            return False

        del self._extensions[extension]
        return True
