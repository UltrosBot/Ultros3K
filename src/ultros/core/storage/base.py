# coding=utf-8

"""
Base classes for storage formats
"""

from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import Any, List, Dict
from weakref import ref

__author__ = "Gareth Coles"


class StorageBase(metaclass=ABCMeta):
    def __init__(self, owner: Any, manager: "ultros.core.storage.manager.StorageManager", path: str,
                 *args: List[Any], **kwargs: Dict[Any, Any]):
        if owner:
            self._owner = ref(owner)
        else:
            self._owner = lambda: None

        self.path = path
        self._manager = ref(manager)
        self.callbacks = []
        self.data = {}

    @property
    def owner(self):
        return self._owner()

    @property
    def manager(self):
        return self._manager()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def reload(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    def run_callbacks(self):
        # TODO: Think about this
        for callback in self.callbacks:
            callback(self)


class MutableStorageBase(StorageBase, AbstractContextManager, metaclass=ABCMeta):
    @abstractmethod
    def save(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not any((exc_type, exc_val, exc_tb)):
            # Everything is None; no errors - we can save

            self.save()


class ItemAccessMixin(metaclass=ABCMeta):
    @abstractmethod
    def __contains__(self, item):
        """
        x in c
        """
        pass

    @abstractmethod
    def __getitem__(self, item):
        """
        c["a"], c[2], c[a:b], c[1:2:3], etc
        """
        pass

    @abstractmethod
    def __iter__(self):
        """
        for x in c
        """
        pass

    @abstractmethod
    def __len__(self):
        """
        len(c)
        """
        pass


class MutableItemAccessMixin(ItemAccessMixin, metaclass=ABCMeta):
    @abstractmethod
    def __delitem__(self, key):
        """
        del c["a"]
        """
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        """
        c["a"] = b
        """
        pass


class DictFunctionsMixin(metaclass=ABCMeta):
    @abstractmethod
    def copy(self):
        """
        Return a shallow copy of the data
        """
        pass

    @abstractmethod
    def get(self, key, default=None):
        """
        Return the data corresponding to the key, or the default value
        if it doesn't exist
        """
        pass

    @abstractmethod
    def items(self):
        """
        Return an iterator or view over (key, value) pairs
        """
        pass

    @abstractmethod
    def keys(self):
        """
        Return an iterator or view of just the keys
        """
        pass

    @abstractmethod
    def values(self):
        """
        Return an iterator or view of just the values
        """
        pass


class MutableDictFunctionsMixin(DictFunctionsMixin, metaclass=ABCMeta):
    @abstractmethod
    def clear(self):
        """
        Delete all stored data
        """
        pass

    @abstractmethod
    def pop(self, key, default=None):
        """
        If a key exists, remove it from the dict and return its value.
        Return the default if it doesn't
        """
        pass

    @abstractmethod
    def popitem(self):
        """
        Pull a (key, value) pair, remove it from storage and return it
        """
        pass

    @abstractmethod
    def setdefault(self, key, default=None):
        """
        Return the value of the key if it exists. If not, set the
        default value to that key and return the value
        """
        pass

    @abstractmethod
    def update(self, other):
        """
        Update your data using the (key, value) pairs of other, overwriting
        as necessary
        """
        pass
