# coding=utf-8
import importlib
import inspect

import os

from ultros.storage.base import StorageBase
from ultros.storage.formats import get_format_from_path

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

        self.data_files = {}
        self.config_files = {}
        self.databases = {}

    def get_data(self, path, owner=None, fmt=None,
                 args: list=None, kwargs: dict=None):
        pass

    def get_config(self, path, owner=None, fmt=None, defaults_path=None,
                   args: list=None, kwargs: dict=None):
        # TODO: Look for a default config file if the given one doesn't exist
        #       If defaults_path is None, append `.default`
        #       If defaults_path is False, don't look for a default
        #       Otherwise, try to use the given defaults_path as the path

        if path in self.config_files:
            # File already loaded at some point
            return self.config_files[path]

        if fmt is None:
            fmt = get_format_from_path(path).config
        else:
            fmt = get_format_from_path(fmt).config

        if fmt is None:
            return  # TODO: Exception

    def get_database(self, path, owner=None, fmt=None,
                     args: list=None, kwargs: dict=None):
        pass

    def unload_data(self, path):
        pass

    def unload_config(self, path):
        pass

    def unload_database(self, path):
        pass

    def unload_for_owner(self, owner):
        pass

    def unload_all(self):
        pass

    def get_class(self, package):
        module = importlib.import_module(package)

        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls):
                for parent in inspect.getmro(cls):
                    if parent == StorageBase:
                        return cls
