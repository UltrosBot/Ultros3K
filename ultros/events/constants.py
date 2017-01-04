# coding=utf-8
"""
Constants for use with the event manager
"""

from enum import IntEnum, unique

__author__ = "Gareth Coles"


@unique
class EventPriority(IntEnum):
    """
    A set of priorities for use with the event manager. Events are run in order
    from lowest priority to highest.

    :ivar LOWEST: :code:`-100`
    :ivar LOW: :code:`-50`
    :ivar NORMAL: :code:`0`
    :ivar HIGH: :code:`50`
    :ivar HIGHEST: :code:`100`
    """

    HIGHEST = 100
    HIGH = 50
    NORMAL = 0
    LOW = -50
    LOWEST = -100
