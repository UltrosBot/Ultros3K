# coding=utf-8

"""
Class for YAML-based (non-roundtrip) configurations
"""

from ruamel import yaml

from typing import Any, List, Dict

from ultros.core.storage import manager as m
from ultros.core.storage.base import AbstractItemAccessMixin, AbstractDictFunctionsMixin
from ultros.core.storage.config.base import ConfigFile

__author__ = "Gareth Coles"


class YAMLConfig(ConfigFile, AbstractItemAccessMixin, AbstractDictFunctionsMixin):
    """
    Class for YAML-based (non-roundtrip) configurations
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        self.data = {}

        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        with open(self.path, "r") as fh:
            self.data = yaml.safe_load(fh, version=(1, 2))

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
