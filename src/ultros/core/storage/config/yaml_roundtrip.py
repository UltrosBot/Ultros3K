# coding=utf-8

"""
Class for YAML-based (roundtrip) configurations

This is a mutable configuration that keeps track of both structure and comments, and allows you to add comments
in certain circumstances as well.

To make use of this, make sure you use the `fmt` argument of the `get_config()` function in the storage manager. For
example:

>>> manager = ultros.storage_manager
>>> config_obj = manager.get_config("test.yml", fmt="yaml-roundtrip")
>>>

"""

from typing import Any, List, Dict

from ruamel import yaml
from ruamel.yaml.comments import CommentedMap, NoComment

from ultros.core.storage import manager as m
from ultros.core.storage.base import MutableAbstractDictFunctionsMixin, MutableAbstractItemAccessMixin
from ultros.core.storage.config.base import MutableConfigFile

__author__ = "Gareth Coles"


class YAMLRoundtripConfig(MutableConfigFile, MutableAbstractItemAccessMixin, MutableAbstractDictFunctionsMixin):
    """
    Class for YAML-based (roundtrip) configurations
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        self.data = CommentedMap()

        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        with open(self.path, "r") as fh:
            self.data = yaml.round_trip_load(fh, version=(1, 2))

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        self.data.clear()

    def save(self):
        if not self.mutable:
            raise RuntimeError("You may not modify a defaults file at runtime - check the mutable attribute!")

        with open(self.path, "w") as fh:
            yaml.round_trip_dump(self.data, fh)

    # region: CommentedMap functions

    def insert(self, pos, key, value, *, comment=None):
        """
        Insert a `key: value` pair at the given position, attaching a comment if provided

        Wrapper for `CommentedMap.insert()`
        """

        return self.data.insert(pos, key, value, comment)

    def add_eol_comment(self, comment, *, key=NoComment, column=30):
        """
        Add an end-of-line comment for a key at a particular column (30 by default)

        Wrapper for `CommentedMap.yaml_add_eol_comment()`
        """

        # Setting the column to None as the API actually defaults to will raise an exception, so we have to
        # specify one unfortunately

        return self.data.yaml_add_eol_comment(comment, key=key, column=column)

    def set_comment_before_key(self, key, comment, *, indent=0):
        """
        Set a comment before a given key

        Wrapper for `CommentedMap.yaml_set_comment_before_after_key()`
        """

        return self.data.yaml_set_comment_before_after_key(
            key, before=comment, indent=indent, after=None, after_indent=None
        )

    def set_start_comment(self, comment, indent=0):
        """
        Set the starting comment

        Wrapper for `CommentedMap.yaml_set_start_comment()`
        """

        return self.data.yaml_set_start_comment(comment, indent=indent)

    # endregion

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
