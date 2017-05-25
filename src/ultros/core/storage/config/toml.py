# coding=utf-8

"""
Class for TOML-based configurations
"""

import toml

from typing import Any, List, Dict

from ultros.core.storage.base import ItemAccessMixin, DictFunctionsMixin
from ultros.core.storage.config.base import ConfigFile

from ultros.core.storage import manager as m

__author__ = "Gareth Coles"


class TOMLConfig(ConfigFile, ItemAccessMixin, DictFunctionsMixin):
    """
    Class for TOML-based configurations
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        self.data = {}

        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        self.data = toml.load(self.path)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self.data.clear()

    # region: Dict functions

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def copy(self):
        return self.data.copy()

    def items(self):
        return self.data.items()

    # endregion

    # Item access functions

    def __contains__(self, key):
        """
        Wrapper for `dict.__contains__()`
        """

        return self.data.__contains__(key)

    def __getitem__(self, key):
        """
        Wrapper for `dict.__getitem__()`
        """

        return self.data.__getitem__(key)

    def __iter__(self):
        """
        Wrapper for `dict.__iter__()`
        """

        return self.data.__iter__()

    def __len__(self):
        """
        Wrapper for `dict.__len__()`
        """

        return self.data.__len__()
