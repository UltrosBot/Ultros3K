# coding=utf-8
"""
Base classes for configuration formats only
"""

import os

from abc import ABCMeta
from typing import Any, List, Dict

from ultros.core.storage.base import StorageBase, MutableStorageBase

__author__ = "Gareth Coles"


class ConfigFile(StorageBase, metaclass=ABCMeta):
    """
    Base class representing any config file
    """

    def __init__(self, owner: Any, manager, path: str, *args: List[Any],
                 **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

        self.path = os.path.join(self.manager.config_location, self.path)

        if not os.path.exists(self.path):
            raise FileNotFoundError()


class MutableConfigFile(ConfigFile, MutableStorageBase, metaclass=ABCMeta):
    """
    Base class representing any *mutable* config file

    Note that mutable config files are not mutable if the filename ends with ".default", and will raise an exception
    if you attempt to call `.save()` - check `.mutable` if you need to be aware of this.
    """

    def __init__(self, owner: Any, manager, path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

        self.mutable = not path.endswith(".default")
