# coding=utf-8
"""
Base classes for database implementations
"""

from abc import ABCMeta
from ultros.core.storage.base import DatabaseStorageBase

__author__ = "Gareth Coles"


class RelationalDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    """
    Class representing a relational database
    """


class DocumentOrientedDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    """
    Class representing a document-oriented database
    """


class OtherDatabase(DatabaseStorageBase, metaclass=ABCMeta):
    """
    Class representing some other kind of database
    """
