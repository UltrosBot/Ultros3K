# coding=utf-8

"""
Base classes for storage formats
"""

from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import Any, List, Dict
from weakref import ref

__author__ = "Gareth Coles"


class StorageBase:
    """
    Base classes that each storage object must inherit at some point to be loadable by the storage manager.

    Currently we have three types of storage - config, data and database. Config and data are both file-backed and
    thus all inherit `FileStorageBase`. Databases are not necessarily file-backed, and inherit DatabaseStorageBase`
    instead.
    """


class DatabaseStorageBase(StorageBase):
    """
    Base class representing any database

    This class has not been finalized yet.
    """


class FileStorageBase(StorageBase, metaclass=ABCMeta):
    """
    Base class representing any storage file

    If you're writing a new storage class, don't subclass this one - subclass one of the relevant
    superclasses from the base modules of the type of storage you're working with. For example,
    `ultros.core.storage.config.base.ConfigFile`.
    """

    def __init__(self, owner: Any, manager, path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        self.mutable = False

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


class MutableFileStorageBase(FileStorageBase, AbstractContextManager, metaclass=ABCMeta):
    """
    Base class representing any mutable storage file

    This provides a default implementation of the context manager protocol that automatically calls `.save()` if
    the context manager is exited without raising any exceptions. We recommend not overriding this unless absolutely
    necessary, as it is expected behavior for all mutable storage files.

    Note that mutable config files are not mutable if the filename ends with ".default", and will raise an exception
    if you attempt to call `.save()` - check `.mutable` if you need to be aware of this.
    """

    def __init__(self, owner: Any, manager, path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

        self.mutable = True

    @abstractmethod
    def save(self):
        """
        Save all stored data to disk

        If you're writing a handler for mutable config files, you should check `.mutable` and raise a RuntimeError
        if it is false instead of saving - this is because defaults files should never be modified at runtime.
        """

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not any((exc_type, exc_val, exc_tb)):
            # Everything is None; no errors - we can save
            if self.mutable:
                self.save()


class AbstractItemAccessMixin(metaclass=ABCMeta):
    """
    A mixin providing abstract methods that are required for item-style data access

    You should implement this if you support `x["something"]` or `x[1:2:3]` for example.
    """

    @abstractmethod
    def __contains__(self, item):
        """
        x in c
        """

    @abstractmethod
    def __getitem__(self, item):
        """
        c["a"], c[2], c[a:b], c[1:2:3], etc
        """

    @abstractmethod
    def __iter__(self):
        """
        for x in c
        """

    @abstractmethod
    def __len__(self):
        """
        len(c)
        """


class MutableAbstractItemAccessMixin(AbstractItemAccessMixin, metaclass=ABCMeta):
    """
    A mixin providing abstract methods that are required for item-style data access and modification

    You should implement this if you support `x["something"] = "other"` for example.
    """

    @abstractmethod
    def __delitem__(self, key):
        """
        del c["a"]
        """

    @abstractmethod
    def __setitem__(self, key, value):
        """
        c["a"] = b
        """


class AbstractDictFunctionsMixin(metaclass=ABCMeta):
    """
    A mixin providing read-only abstract methods that mimic those that are provided by dicts by default

    You should implement this if you want to emulate the behavior of a dict
    """

    @abstractmethod
    def copy(self):
        """
        Return a shallow copy of the data
        """

    @abstractmethod
    def get(self, key, default=None):
        """
        Return the data corresponding to the key, or the default value
        if it doesn't exist
        """

    @abstractmethod
    def items(self):
        """
        Return an iterator or view over (key, value) pairs
        """

    @abstractmethod
    def keys(self):
        """
        Return an iterator or view of just the keys
        """

    @abstractmethod
    def values(self):
        """
        Return an iterator or view of just the values
        """


class MutableAbstractDictFunctionsMixin(AbstractDictFunctionsMixin, metaclass=ABCMeta):
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

    @abstractmethod
    def pop(self, key, default=None):
        """
        If a key exists, remove it from the dict and return its value.
        Return the default if it doesn't
        """

    @abstractmethod
    def popitem(self):
        """
        Pull a (key, value) pair, remove it from storage and return it
        """

    @abstractmethod
    def setdefault(self, key, default=None):
        """
        Return the value of the key if it exists. If not, set the
        default value to that key and return the value
        """

    @abstractmethod
    def update(self, other):
        """
        Update your data using the (key, value) pairs of other, overwriting
        as necessary
        """
