# coding=utf-8

"""
Classes for configuration files

These classes provide a somewhat thin API around various file formats that are expected to be used
for configuration files. Instances of them will be returned by the storage manager on request - you
do not need to instantiate these on your own.

Please note that most of these classes will only provide an immutable API - the only mutable ones
provided must be able to preserve comments, and may need special treatment. Please check the
individual documentation for each one for more information.

Submodules
==========

.. currentmodule:: ultros.core.storage.config

.. autosummary::
    :toctree: config

    base
    ini
"""

__author__ = "Gareth Coles"
