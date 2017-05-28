# coding=utf-8

__author__ = "Gareth Coles"


class StorageManagerError(Exception):
    pass


class UnknownFormatError(StorageManagerError):
    pass


class UnsupportedFormatError(StorageManagerError):
    pass
