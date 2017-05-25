# coding=utf-8

"""
The storage manager, which is in charge of all things storage

This is not a singleton any more! You'll need to get an instance of it
elsewhere.
"""

# TODO: Where to get the instance

import importlib
import inspect
import os

from typing import Optional, Any, Dict, List, Union

from ultros.core import ultros as u
from ultros.core.storage.base import StorageBase, MutableStorageBase, ItemAccessMixin, MutableItemAccessMixin, \
    DictFunctionsMixin, MutableDictFunctionsMixin
from ultros.core.storage.config.base import ConfigFile, MutableConfigFile
from ultros.core.storage.data.base import DataFile
from ultros.core.storage.formats import FileFormats

__author__ = "Gareth Coles"

BASE_CLASSES = [
    StorageBase, MutableStorageBase, ItemAccessMixin, MutableItemAccessMixin, DictFunctionsMixin,
    MutableDictFunctionsMixin, ConfigFile, MutableConfigFile, DataFile
]


class StorageManager:
    """
    The storage manager object, which handles loading and management
    of storage files and database abstraction.

    If you're working with any kinds of files, it is best to use this, as it
    will make sure that your plugin will automatically have its files saved and
    cleaned up when it gets unloaded, and that all files are saved and cleaned
    up when the bot shuts down.

    As this is no longer a Singleton, feel free to instantiate one for your
    own (appropriate) advanced use-cases. When instantiated, it will create
    a new FileFormats object representing the default supported file formats.

    :ivar config_files: Dict of all loaded config files
    :ivar config_location: Path (str) to a directory containing config files

    :ivar databases: Dict of all loaded database abstraction objects

    :ivar data_files: Dict of all loaded data files
    :ivar data_location: Path (str) to a directory containing data files

    :ivar file_formats: A FileFormats object representing all supported formats
    """

    config_location = None
    data_location = None

    config_files = None
    data_files = None
    databases = None

    file_formats = None

    ultros = None

    def __init__(self, ultros: "u.Ultros", config_location: str,
                 data_location: str):
        """
        :param config_location: Path to a directory for config files
        :param data_location: Path to a directory for data files
        """
        self.ultros = ultros

        self.config_location = os.path.normpath(config_location)
        self.data_location = os.path.normpath(data_location)
        self.file_formats = FileFormats()

        self.data_files = {}
        self.config_files = {}
        self.databases = {}

    def shutdown(self):
        try:
            self.unload_all()
        except Exception as e:
            print(e)  # TODO: Logging

        self.ultros = None

    def get_config(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                   defaults_path: Optional[Union[str, bool]]=None,
                   *args: List[Any], **kwargs: Dict[Any, Any]
                   ) -> Optional[StorageBase]:
        """
        Attempts to load a config file (if it isn't already loaded) and
        returns it to you.

        * The **owner** is optional, but should be supplied if you are writing
          a plugin, protocol, or other unloadable object. This allows the file
          to be cleaned up automatically.
        * **defaults_path** is a little complicated, and may be one of three
          value types.

          * **None**: The default; attempt to reload the file if it cannot be
            found by appending :code:`.default` to it.
          * **False**: Fail hard by throwing an exception if the file cannot
            be found.
          * **str**: A path to attempt to load if the file cannot be found.
            This will fail hard with an exception if this second file cannot
            be found.

        :param path: Path to the file, relative to the config directory
        :param owner: Object that owns the file, or None
        :param fmt: An explicit format (represented by an extension) or None to
                    guess it from the path
        :param defaults_path: None (default), a str or False. See above.
        :param args: Extra arguments to pass to the underlying storage object
        :param kwargs: Extra keyword arguments to pass to the underlying
                       storage object
        :return: A storage object, or None if the format isn't found or
                 doesn't support config files, or the file isn't found and an
                 invalid value is supplied for defaults_path (these will be
                 exceptions later)
        """  # TODO: Edit this when we use exceptions

        if path in self.config_files:
            # File already loaded at some point
            return self.config_files[path]

        if fmt is None:  # Guess based on extension
            _fmt = self.file_formats.get_format_from_path(path)
        else:  # Extension was given
            _fmt = self.file_formats.get_format_from_path(fmt)

        if _fmt is None:  # No idea what that extension is
            return  # TODO: Exception

        _fmt = _fmt.config

        if _fmt is None:  # Format doesn't support config files
            return  # TODO: Exception (using fmt.name)

        format_cls = self.get_class(_fmt)

        try:
            obj = format_cls(owner, self, path, *args, **kwargs)  # TODO: Params
            obj.load()
        except FileNotFoundError:  # Handle default config files
            if defaults_path is None:
                return self.get_config(
                    path + ".default", owner, _fmt,
                    defaults_path=False, *args, **kwargs
                )
            elif not defaults_path:
                raise
            elif isinstance(defaults_path, str):
                return self.get_config(
                    defaults_path, owner, _fmt,
                    defaults_path=False, *args, **kwargs
                )
            else:
                pass  # TODO: Exception

        else:
            self.config_files[path] = obj

            return obj

    def get_data(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                 *args: List[Any], **kwargs: Dict[Any, Any]
                 ) -> Optional[MutableStorageBase]:
        """
        Attempts to load a data file (if it isn't already loaded) and
        returns it to you.

        * The **owner** is optional, but should be supplied if you are writing
          a plugin, protocol, or other unloadable object. This allows the file
          to be cleaned up automatically.

        :param path: Path to the file, relative to the data directory
        :param owner: Object that owns the file, or None
        :param fmt: An explicit format (represented by an extension) or None to
                    guess it from the path
        :param args: Extra arguments to pass to the underlying storage object
        :param kwargs: Extra keyword arguments to pass to the underlying
                       storage object
        :return: A storage object, or None if the format isn't found or
                 doesn't support config files (these will be exceptions later)
        """  # TODO: Edit this when we use exceptions

        if path in self.data_files:
            # File already loaded at some point
            return self.data_files[path]

        if fmt is None:  # Guess based on extension
            _fmt = self.file_formats.get_format_from_path(path)
        else:  # Extension was given
            _fmt = self.file_formats.get_format_from_path(fmt)

        if _fmt is None:  # No idea what that extension is
            return  # TODO: Exception

        _fmt = _fmt.data

        if _fmt is None:  # Format doesn't support data files
            return  # TODO: Exception (using fmt.name)

        format_cls = self.get_class(_fmt)
        obj = format_cls(owner, self, path, *args, **kwargs)  # TODO: Params
        obj.load()

        self.data_files[path] = obj

        return obj

    def get_database(self, path: str, owner: Any=None, fmt: Optional[str]=None,
                     args: List[Any]=None, kwargs: Dict[Any, Any]=None
                     ) -> StorageBase:
        """
        This function has not been finalized yet.

        :param path:
        :param owner:
        :param fmt:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def unload_data(self, path: str) -> bool:
        """
        Unload a data file by path, regardless of the state of the owner.

        :param path: The path of the file to unload
        :return: True if the file was unloaded (it was loaded), False otherwise
        """
        pass

    def unload_config(self, path: str) -> bool:
        """
        Unload a config file by path, regardless of the state of the owner.

        :param path: The path of the file to unload
        :return: True if the file was unloaded (it was loaded), False otherwise
        """
        pass

    def unload_database(self, path: str) -> bool:
        """
        This function has not been finalized yet.

        :param path:
        :return:
        """
        pass

    def unload_for_owner(self, owner: Any) -> bool:
        """
        Unload all config and data files and database abstractions owned by
        an object. This will never unload files that don't have an owner - even
        if you pass in None for it.

        :param owner: The owning object to unload storage objects for
        :return: Whether any files were unloaded
        """
        if owner is None:
            return False

        pass

    def unload_all(self):
        """
        Unload every file currently loaded by this manager. This should always
        be called to clean up when you're done with the manager.
        """
        pass

    def get_class(self, package: str) -> Optional[type(StorageBase)]:
        """
        Load a storage object class by searching for it within a given module.

        This will traverse the members of the module, looking for the first
        class that subclasses StorageBase, and returns the class object (not
        an instance of the class).

        :param package: The module to search within
        :return: The discovered class, or None if no eligible class was found
        """

        module = importlib.import_module(package)

        for name, format_cls in inspect.getmembers(module):
            if inspect.isclass(format_cls):
                if format_cls not in BASE_CLASSES:
                    for parent in inspect.getmro(format_cls):
                        if parent == StorageBase:
                            return format_cls
