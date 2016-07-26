# coding=utf-8
import importlib
import inspect
import os

from typing import Optional, Any, Dict, List, Union

from ultros.storage.base import StorageBase
from ultros.storage.formats import Formats

__author__ = "Gareth Coles"


class StorageManager:
    config_location = None
    data_location = None

    data_files = None
    config_files = None
    databases = None

    def __init__(self, config_location, data_location):
        self.config_location = os.path.normpath(config_location)
        self.data_location = os.path.normpath(data_location)
        self.formats = Formats()

        self.data_files = {}
        self.config_files = {}
        self.databases = {}

    def get_data(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                 args: List[Any]=None, kwargs: Dict[Any, Any]=None
                 ) -> StorageBase:
        if path in self.data_files:
            # File already loaded at some point
            return self.data_files[path]

        if fmt is None:  # Guess based on extension
            fmt = self.formats.get_format_from_path(path)
        else:  # Extension was given
            fmt = self.formats.get_format_from_path(fmt)

        if fmt is None:  # No idea what that extension is
            return  # TODO: Exception

        fmt = fmt.data

        if fmt is None:  # Format doesn't support data files
            return  # TODO: Exception (using fmt.name)

        cls = self.get_class(fmt)

    def get_config(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                   defaults_path: Optional[Union[str, bool]]=None,
                   args: List[Any]=None, kwargs: Dict[Any, Any]=None
                   ) -> StorageBase:

        if path in self.config_files:
            # File already loaded at some point
            return self.config_files[path]

        if fmt is None:  # Guess based on extension
            _fmt = self.formats.get_format_from_path(path)
        else:  # Extension was given
            _fmt = self.formats.get_format_from_path(fmt)

        if _fmt is None:  # No idea what that extension is
            return  # TODO: Exception

        _fmt = _fmt.config

        if _fmt is None:  # Format doesn't support config files
            return  # TODO: Exception (using fmt.name)

        cls = self.get_class(_fmt)

        try:
            obj = cls(owner)  # TODO: Params
        except FileNotFoundError:
            if defaults_path is None:
                return self.get_config(
                    path + ".default", owner, fmt,
                    defaults_path=False, args=args, kwargs=kwargs
                )
            elif not defaults_path:
                raise
            elif isinstance(defaults_path, str):
                return self.get_config(
                    defaults_path, owner, fmt,
                    defaults_path=False, args=args, kwargs=kwargs
                )
            else:
                pass  # TODO: Exception

        else:
            self.config_files[path] = obj

            return obj

    def get_database(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                     args: List[Any]=None, kwargs: Dict[Any, Any]=None
                     ) -> StorageBase:
        pass

    def unload_data(self, path: str):
        pass

    def unload_config(self, path: str):
        pass

    def unload_database(self, path: str):
        pass

    def unload_for_owner(self, owner: Any):
        pass

    def unload_all(self):
        pass

    def get_class(self, package: str) -> type:
        module = importlib.import_module(package)

        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls):
                for parent in inspect.getmro(cls):
                    if parent == StorageBase:
                        return cls
