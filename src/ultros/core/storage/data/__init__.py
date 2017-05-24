# coding=utf-8

"""
Classes for data files

These classes provide a somewhat thin API around various file formats that are expected to be used
for data files. Instances of them will be returned by the storage manager on request - you
do not need to instantiate these on your own.

As data files are expected to be modified often, these classes all provide mutable APIs. Instead of
providing complex access mechanisms, however, you may simply use them as a context manager for ease
of use. For example:

>>> x = ultros.storage_manager.get_data("test.yml")
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

.. currentmodule:: ultros.core.storage.data

.. autosummary::
    :toctree: data

    base
"""

__author__ = "Gareth Coles"
