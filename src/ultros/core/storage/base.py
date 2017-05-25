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
    """
    Base class representing any storage file

    If you're writing a new storage class, don't subclass this one - subclass one of the relevant
    superclasses from the base modules of the type of storage you're working with. For example,
    `ultros.core.storage.config.base.ConfigFile`.
    """

    def __init__(self, owner: Any, manager, path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
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
        """
        Load up all needed data

        This will be called by the storage manager automatically
        """

    @abstractmethod
    def reload(self):
        """
        Reload all needed data
        """

    @abstractmethod
    def unload(self):
        """
        Unload all stored data
        """

    def run_callbacks(self):
        """
        Run all callbacks registered for this storage object

        This function is not finalized.
        """
        # TODO: Think about this
        for callback in self.callbacks:
            callback(self)


class MutableStorageBase(StorageBase, AbstractContextManager, metaclass=ABCMeta):
    """
    Base class representing any mutable storage file

    This provides a default implementation of the context manager protocol that automatically calls `.save()` if
    the context manager is exited without raising any exceptions. We recommend not overriding this unless absolutely
    necessary, as it is expected behavior for all mutable storage files.
    """

    @abstractmethod
    def save(self):
        """
        Save all stored data to disk
        """

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not any((exc_type, exc_val, exc_tb)):
            # Everything is None; no errors - we can save

            self.save()


class ItemAccessMixin(metaclass=ABCMeta):
    """
    A mixin providing abstract methods that are required for item-style data access

    You should implement this if you support `x["something"]` or `x[1:2:3]` for example.
    """

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
    """
    A mixin providing abstract methods that are required for item-style data access and modification

    You should implement this if you support `x["something"] = "other"` for example.
    """

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
    """
    A mixin providing read-only abstract methods that mimic those that are provided by dicts by default

    You should implement this if you want to emulate the behavior of a dict
    """

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
    """
    A mixin providing abstract methods that mimic those that are provided by dicts by default, including those that
    modify the dict

    You should implement this if you want to emulate the behavior of a dict
    """

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
