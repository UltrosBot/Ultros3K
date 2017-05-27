# coding=utf-8

"""
Class for YAML-based data files
"""
import os

from ruamel import yaml
from typing import Any, List, Dict

from ultros.core.storage import manager as m
from ultros.core.storage.base import MutableAbstractDictFunctionsMixin, MutableAbstractItemAccessMixin
from ultros.core.storage.data.base import DataFile

__author__ = "Gareth Coles"


class YAMLData(DataFile, MutableAbstractItemAccessMixin, MutableAbstractDictFunctionsMixin):
    """
    Class for YAML-based data files
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        self.data = {}

        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as fh:
                self.data = yaml.load(fh, version=(1, 2))
        else:
            self.data = {}

    def save(self):
        with open(self.path, "w") as fh:
            yaml.dump(self.data, fh)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self.clear()

    # region: Dict functions

    def clear(self):
        return self.data.clear()

    def copy(self):
        return self.data.copy()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def pop(self, key, default=None):
        return self.data.pop(key, default)

    def popitem(self):
        return self.data.popitem()

    def setdefault(self, key, default=None):
        if key not in self.data:
            self.data[key] = default
            return default

        return self.data[key]

    def update(self, other):
        return self.data.update(other)

    def values(self):
        return self.data.values()

    # endregion

    # Item access functions

    def __contains__(self, key):
        """
        Wrapper for `dict.__contains__()`
        """

        return self.data.__contains__(key)

    def __delitem__(self, key):
        """
        Wrapper for `dict.__delitem__()`
        """

        del self.data[key]

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

    def __setitem__(self, key, value):
        """
        Wrapper for `dict.__getitem__()`
        """

        return self.data.__setitem__(key, value)
