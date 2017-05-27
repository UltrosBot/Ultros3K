#  coding=utf-8

"""
Class for INI-based data files
"""
import os

from configparser import ConfigParser, _UNSET
from typing import Any, List, Dict, Union

from ultros.core.storage import manager as m
from ultros.core.storage.base import MutableAbstractItemAccessMixin
from ultros.core.storage.data.base import DataFile

__author__ = "Gareth Coles"


class INIData(DataFile, MutableAbstractItemAccessMixin):
    """
    Class for INI-based data files
    """

    def __init__(self, owner: Any, manager: "m.StorageManager", path: str, *args: List[Any], **kwargs: Dict[Any, Any]):
        super().__init__(owner, manager, path, *args, **kwargs)

    def load(self):
        if os.path.exists(self.path):
            self.data = ConfigParser()
            self.data.read(self.path)

    def reload(self):
        self.unload()
        self.load()

    def unload(self):
        del self.data

    def save(self):
        with open(self.path, "w") as fh:
            self.data.write(fh)

    # region: ConfigParser methods

    def sections(self):
        """
        Return a list of the sections available; the "DEFAULT" section is not included in the list.
        """

        return self.data.sections()

    def add_section(self, section: str):
        """
        Add a section named `section` to the instance.

        If a section by the given name already exists, raises `DuplicateSectionError`.
        If the default section name is passed, raises `ValueError`.
        The name of the section must be a string, otherwise `TypeError` is raised.
        """

        return self.data.add_section(section)

    def has_section(self, section: str):
        """
        Indicates whether the named `section` is present. The "DEFAULT" section is not acknowledged.
        """

        return self.data.has_section(section)

    def options(self, section: str):
        """
        Returns a list of options available in the specified `section`.
        """

        return self.data.options(section)

    def has_option(self, section: str, option: str):
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

        * For True: `1`, `yes`, `true`, `on`
        * For False: `0`, `no`, `false`, `off`

        Anything else will return a ValueError.
        """

        return self.data.getboolean(section, option, raw=raw, vars=vars, fallback=fallback)

    def items(self, section: str=_UNSET, raw=False, vars=None):
        """
        When `section` is not given, return a list of (*section_name*, *section_proxy*) pairs, including the "DEFAULT"
        section. Otherwise, return a list of (*name*, *value*) pairs for the options in the given `section`.

        Optional arguments have the same meaning as for the `get` method.
        """

        if section == _UNSET:
            return self.data.items(raw=raw, vars=vars)
        return self.data.items(section, raw=raw, vars=vars)

    def set(self, section: str, option: str, value: str):
        """
        If the given `section` exists, set the given option to the specified value; otherwise raise `NoSectionError`.

        Note that `option` and `value` must be strings - if not, `TypeError` is raised.
        """

        return self.data.set(section, option, value)

    def remove_option(self, section: str, option: str):
        """
        Remove the specified `option` from the specified `section`.

        If the section does not exists, raises `NoSectionError`.
        If the option existed, returns `True`, otherwise returns `False`.
        """

        return self.data.remove_option(section, option)

    def remove_section(self, section: str):
        """
        Remove the specified `section` from the instance.

        If the section existed, returns `True`, otherwise returns `False`.
        """

        return self.data.remove_section(section)

    # endregion

    # Item access functions

    def __contains__(self, item: str):
        """
        This is called for an "x in y" check, and will check whether a section exists.
        """

        return self.data.has_section(item)

    def __getitem__(self, item: Union[str, slice]):
        """
        This is called for dict-like item access, eg `x["item"]`.

        Passing in a string here will return a ConfigParser section (which generally works like a dict too). However,
        you may also pass in a simple slice to get a specific option within a section.

        >>> x = ultros.core.storage_manager.get_data("test.ini")
        >>> x["x"]
        {"y": "z"}
        >>> x["x":"y"]
        "z"
        >>>

        Note that this will not cast the value at all - as usual, the value will be a string. If you want the
        ConfigParser to cast for you, use one of the "getX" methods.
        """

        if isinstance(item, slice):  # x[section:option]
            return self.get(item.start, item.stop)

        return self.data[item]

    def __delitem__(self, item):
        """
        This is called for dict-like item deletion, eg `del x["item"]`.

        Passing in a string here will delete the section with the matching name. However, you may also pass in a
        simple slice to delete a specific option within a section.

        >>> x = ultros.core.storage_manager.get_data("test.ini")
        >>> x["x"]
        {"y": "z"}
        >>> del x["x":"y"]
        >>> x["x"]
        {}
        >>>

        As usual, make sure all your values are strings. Exceptions will be raised in accordance with `remove_section`
        and `remove_option`.
        """

        if isinstance(item, slice):  # x[section:option]
            return self.remove_option(item.start, item.stop)

        return self.remove_section(item)

    def __setitem__(self, item, value):
        """
        This is called for dict - like item addition, eg `x["item"] = {}`.

        Passing in a string here will allow you to initialise a section using a new dictionary. Note that all keys
        and values must be strings - and passing in anything but a dictionary will raise `TypeError`. Note: this will
        overwrite existing sections.

        You may also pass in a slice if you just want to set an option within a specific section. If the section
        doesn't exist, `NoSectionError` will be raised.

        >>> x = ultros.core.storage_manager.get_data("test.ini")
        >>> x["x"] = {"y": "z"}
        >>> x["x"]
        {"y": "z"}
        >>> x["x":"a"] = "b"
        >>> x["x"]
        {"y": "z", "a": "b"}
        >>>
        """

        if isinstance(item, slice):
            return self.set(item.start, item.stop, value)
        elif isinstance(item, str):
            if isinstance(value, dict):
                self.data[item] = value
                return

            raise TypeError("You may only initialize a section using a dict.")

        raise TypeError("You may only use a string or simple slice as a key.")

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
