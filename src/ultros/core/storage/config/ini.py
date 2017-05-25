# coding=utf-8

"""
Class for INI-based configurations
"""

import os

from configparser import ConfigParser, _UNSET
from typing import Any, List, Dict, Union

from ultros.core.storage.base import ItemAccessMixin
from ultros.core.storage.config.base import ConfigFile

from ultros.core.storage import manager as m

__author__ = "Gareth Coles"


class INIConfig(ConfigFile, ItemAccessMixin):
    """
    Class for INI-based configurations
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        self.data = ConfigParser()
        self.data.read(self.path)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        del self.data

    # region: ConfigParser methods

    def sections(self):
        """
        Return a list of the sections available; the "DEFAULT" section is not included in the list.
        """

        return self.data.sections()

    def has_section(self, section):
        """
        Indicates whether the named `section` is present. The "DEFAULT" section is not acknowledged.
        """

        return self.data.has_section(section)

    def options(self, section):
        """
        Returns a list of options available in the specified `section`.
        """

        return self.data.options(section)

    def has_option(self, section, option):
        """
        If the given `section` exists, and contains the given `option`, return `True`; otherwise return `False`.
        If the specified `section` is `None` or an empty string, "DEFAULT" is assumed.
        """

        return self.data.has_option(section, option)

    def get(self, section: str, option: str, *, raw=False, vars: dict=None, fallback=_UNSET) -> str:
        """
        Get an option value for a given section.

        The option is looked up in `vars` (if provided), `section`, and in the "DEFAULT" section in that order.
        If the key is not found and `fallback` is provided, it is used as a fallback value. `None` can be provided as
        a `fallback` value.

        If `raw` is True, then interpolations are not expanded in the return values.
        """

        return self.data.get(section, option, raw=raw, vars=vars, fallback=fallback)

    def get_int(self, section: str, option: str, *, raw=False, vars: dict=None, fallback=_UNSET) -> int:
        """
        Same as `get`, but the result will be coerced to an `int`.
        """

        return self.data.getint(section, option, raw=raw, vars=vars, fallback=fallback)

    def get_float(self, section: str, option: str, *, raw=False, vars: dict=None, fallback=_UNSET) -> float:
        """
        Same as `get`, but the result will be coerced to a `float`.
        """

        return self.data.getfloat(section, option, raw=raw, vars=vars, fallback=fallback)

    def get_boolean(self, section: str, option: str, *, raw=False, vars: dict=None, fallback=_UNSET) -> bool:
        """
        Same as `get`, but the result will be coerced to a `bool`.

        Note that different values for the option are accepted here and will affect the return value..

        For True: `1`, `yes`, `true`, `on`
        For False: `0`, `no`, `false`, `off`

        Anything else will return a ValueError.
        """

        return self.data.getboolean(section, option, raw=raw, vars=vars, fallback=fallback)

    def items(self, section=_UNSET, raw=False, vars=None):
        """
        When `section` is not given, return a list of (*section_name*, *section_proxy*) pairs, including the "DEFAULT"
        section. Otherwise, return a list of (*name*, *value*) pairs for the options in the given `section`.

        Optional arguments have the same meaning as for the `get` method.
        """

        if section == _UNSET:
            return self.data.items(raw=raw, vars=vars)
        return self.data.items(section, raw=raw, vars=vars)

    # endregion

    # Item access functions

    def __contains__(self, item: str):
        """
        This is called for an "x in y" check, and will check whether a section exists.
        """

        return self.data.has_section(item)

    def __getitem__(self, item: Union[str, slice]):
        """
        This is called for dict-like item access, eg x["item"].

        Passing in a string here will return a ConfigParser section (which generally works like a dict too). However,
        you may also pass in a simple slice to get a specific option within a section.

        >>> x = ultros.core.storage_manager.get_config("test.ini")
        >>> x["x"]
        {"y": "z"}
        >>> x["x":"y"]
        "z"
        >>>

        Note that this will not cast the value at all - as usual, the value will be a string. If you want the
        ConfigParser to cast for you, use one of the "getX" methods.
        """

        if isinstance(item, slice):  # x[section:option]
            return self.data.get(item.start, item.stop)

        return self.data[item]

    def __iter__(self):
        """
        Wrapper for `ConfigParser.__iter__()`
        """

        return self.data.__iter__()

    def __len__(self):
        """
        Wrapper for `ConfigParser.__len__()`
        
        Note that the default section is always counted, whether it exists or not.
        """

        return self.data.__len__()
