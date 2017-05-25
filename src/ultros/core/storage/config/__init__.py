# coding=utf-8

"""
Classes for configuration files

These classes provide a somewhat thin API around various file formats that are expected to be used
for configuration files. Instances of them will be returned by the storage manager on request - you
do not need to instantiate these on your own.

Please note that most of these classes will only provide an immutable API - the only mutable ones
provided must be able to preserve comments, and may need special treatment. Please check the
individual documentation for each one for more information.

As with all data files, any mutable config files may simply be used as a context manager
instead of worrying about complicated access mechanisms. For example:

>>> x = ultros.core.storage_manager.get_config("test.yml-roundtrip")
>>> with x:
...     x[1] = 2
...     x["a"]["b"] = "c"
...
>>> x.reload()
>>> x[1]
2  # The file has been saved automatically upon exiting the context manager
>>>


Note that the file *will not be saved* if an exception is raised within the context manager. If this
isn't your intention, then remember to handle any exceptions yourself.

Submodules
==========

.. currentmodule:: ultros.core.storage.config

.. autosummary::
    :toctree: config

    base
    ini
    json
    python
    toml
"""

__author__ = "Gareth Coles"
