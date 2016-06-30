# coding=utf-8

__author__ = 'Gareth Coles'


class InstanceManager:
    _instance = None

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super(InstanceManager, cls).__new__(
                cls, *args
            )

        return cls._instance
