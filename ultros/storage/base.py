# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Any
from weakref import ref

__author__ = "Gareth Coles"


class StorageBase(metaclass=ABCMeta):
    def __init__(self, owner: Any):
        self._owner = ref(owner)
        self.callbacks = []
        self.data = {}

    @property
    def owner(self):
        return self._owner()

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def reload(self):
        pass

    def run_callbacks(self):
        # TODO: Think about this
        for callback in self.callbacks:
            callback(self)


class MutableStorageBase(StorageBase):
    @abstractmethod
    def save(self):
        pass
