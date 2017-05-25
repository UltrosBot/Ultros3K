# coding=utf-8
"""
Base classes for data formats only
"""
import os
from abc import ABCMeta
from typing import Any, List, Dict

from ultros.core.storage.base import MutableStorageBase

__author__ = "Gareth Coles"


class DataFile(MutableStorageBase, metaclass=ABCMeta):
    """
    Base class representing any data file
    """

    def __init__(self, owner: Any, manager: "ultros.core.storage.manager.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

        self.path = os.path.join(self.manager.data_location, self.path)
