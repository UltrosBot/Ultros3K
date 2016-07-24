# coding=utf-8
from enum import IntEnum, unique

__author__ = "Gareth Coles"


@unique
class EventPriority(IntEnum):
    HIGHEST = 100
    HIGH = 50
    NORMAL = 0
    LOW = -50
    LOWEST = -100
