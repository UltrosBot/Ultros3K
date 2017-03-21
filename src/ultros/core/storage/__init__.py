# coding=utf-8

"""
Storage management and format definitions

This module contains all of our code relating to file-based and database-based
storage. If you're accessing any kind of configuration, data files, or
databases, then you should do it through this module. This allows us
to keep track of any open files/database connections, making them available
to management plugins and cleaning them up when they're no longer used.

If we're missing a format or feature that you need, feel free to open a ticket
or submit a pull request.

Submodules
==========

.. currentmodule:: ultros.core.storage

.. autosummary::
    :toctree: storage

    config
    data
    database
    formats
    manager
"""

__author__ = "Gareth Coles"
