# coding=utf-8

"""
Base classes for configuration formats only
"""

from abc import ABCMeta
from ultros.core.storage.base import StorageBase, MutableStorageBase

__author__ = "Gareth Coles"


class ConfigFile(StorageBase, metaclass=ABCMeta):
    """
    Base class representing any config file
    """
    pass


class MutableConfigFile(ConfigFile, MutableStorageBase, metaclass=ABCMeta):
    """
    Base class representing any *mutable* config file
    """
    pass
