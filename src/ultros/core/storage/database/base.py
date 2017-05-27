# coding=utf-8
from abc import ABCMeta

from ultros.core.storage.base import DatabaseStorageBase

__author__ = "Gareth Coles"


class RelationalDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    pass


class DocumentOrientedDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    pass


class OtherDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    pass
