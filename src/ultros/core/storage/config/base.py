# coding=utf-8

"""
Base classes for configuration formats only

Members
=======
"""

from abc import ABCMeta
from ultros.core.storage.base import StorageBase, MutableStorageBase

__author__ = "Gareth Coles"


class ConfigFile(StorageBase, metaclass=ABCMeta):
    pass


class MutableConfigFile(ConfigFile, MutableStorageBase, metaclass=ABCMeta):
    pass
