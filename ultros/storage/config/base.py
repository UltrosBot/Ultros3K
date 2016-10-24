# coding=utf-8
from ultros.storage.base import StorageBase, MutableStorageBase

__author__ = "Gareth Coles"


class ConfigFile(StorageBase):
    pass


class MutableConfigFile(ConfigFile, MutableStorageBase):
    pass
