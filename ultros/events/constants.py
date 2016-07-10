# coding=utf-8
from enum import IntEnum

__author__ = 'Gareth Coles'


class EventPriority(IntEnum):
    HIGHEST = 2
    HIGH = 1
    NORMAL = 0
    LOW = -1
    LOWEST = -2
