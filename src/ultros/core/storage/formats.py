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

CONF = "conf"
INI = "ini"
JSON = "json"
PYTHON = "py"
TOML = "toml"
YML = "yml"
YML_ROUNDTRIP = "yml-roundtrip"

# Constants for database type names

DB_SQLALCHEMY = "sqlalchemy"


class DatabaseFormats:
    """
    Contains information about what databases are supported and where to look for a class that can handle
    that database.
    
    Each database type is associated with a keyword, and that points to a package containing the relevant class.
    When a database implementation is requested from the storage manager, it will load the module and scan it for
    the first class that implements StorageBase. That class is then instantiated and used as the storage object.
    """

    def __init__(self):
        self._databases = {
            DB_SQLALCHEMY: "ultros.core.storage.database.sqla"
        }

    def get_format(self, name):
        return self._databases.get(name)

    def add_format(self, name: str, module: str) -> bool:
        """
        Register a supported format, if the it hasn't already been registered.
        
        :return: False if the format was already registered, otherwise True
        """

        if name in self._databases:
            return False

        self._databases[name] = module
        return True

    def remove_format(self, name: str) -> bool:
        """
        Remove an already-registered format by name, if it exists.

        :return: False if the format isn't registered, True otherwise
        """

        if name not in self._databases:
            return False

        del self._databases[name]
        return True


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
    | .yml           | YAML                      | Config & Data |
    +----------------+---------------------------+---------------+
    | .yml-roundtrip | YAML (round-trip parser)  | Config only   |
    +----------------+---------------------------+---------------+
    """

    def __init__(self):
        self._extensions = {
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
