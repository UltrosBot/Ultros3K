# coding=utf-8


"""
Base classes for data formats only

Members
=======
"""

from abc import ABCMeta
from ultros.core.storage.base import MutableStorageBase

__author__ = "Gareth Coles"


class DataFile(MutableStorageBase, metaclass=ABCMeta):
    pass
