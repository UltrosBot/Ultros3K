# coding=utf-8

"""
Constants for use with the rules engine.
"""

from enum import IntEnum

__author__ = 'Gareth Coles'


class TransformerResult(IntEnum):
    """
    Represents what to do after a transformer has been run. Transformers must
    return one of the following:

    * RETURN - Stop processing rules. This can be returned within a tuple that
      also contains another value to return.
    * CONTINUE - Move on to the next rule.
    """

    RETURN = 0
    CONTINUE = 1
