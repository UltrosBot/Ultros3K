# coding=utf-8

"""
A module for a predefined set of basic predicates.

A predicate is a condition - They take two arguments and return either True
or False. The left side, `value`, is the value being compared currently, the
value the current set of rules is being applied to. The right side,
`comparable`, is the comparison value that has been specified in the rule
that's currently being checked.

Aside from that, predicates can do whatever they want, but do bear in mind
that they are only designed to be used for checking, not actioning. Note that
predicates may either be a standard function, or a coroutine function.
"""

import re

from numbers import Number
from typing import Union

__author__ = "Gareth Coles"


# Number operations

def num_greater_than(value: Number, comparable: Number) -> bool:
    """
    Checks whether `value` is greater than `comparable`.
    """

    return value > comparable


def num_less_than(value: Number, comparable: Number) -> bool:
    """
    Checks whether `value` is less than `comparable`.
    """

    return value < comparable


# String operations

def str_contains(value: str, comparable: str) -> bool:
    """
    Checks whether `value` contains `comparable`.
    """

    return value in comparable


def str_matches_regex(value: str,
                      comparable: Union[str, re._pattern_type]) -> bool:
    """
    Checks whether `value` matches the regex stored in `comparable`.
    """

    return re.match(comparable, value)


def str_not_contains(value: str, comparable: str) -> bool:
    """
    Checks whether `value` doesn't contain `comparable`.
    """

    return value not in comparable


def str_not_matches_regex(value: str,
                          comparable: Union[str, re._pattern_type]) -> bool:
    """
    Checks whether `value` doesn't match the regex stored in `comparable`.
    """

    return not re.match(comparable, value)


# Generic object operations

def equal(value: object, comparable: object) -> bool:
    """
    Checks whether `value` equals `comparable`.
    """

    return value == comparable


def identical(value: object, comparable: object) -> bool:
    """
    Checks whether `value` has the same identity as `comparable`.
    """

    return value is comparable


def not_equal(value: object, comparable: object) -> bool:
    """
    Checks whether `value` is not equal to `comparable`.
    """

    return value != comparable


def not_identical(value: object, comparable: object) -> bool:
    """
    Checks whether `value` has a different identity to `comparable`.
    """

    return value is not comparable


def is_instance(value: object, comparable: type) -> bool:
    """
    Checks whether `value` is an instance of `comparable`.
    """

    return isinstance(value, comparable)


def is_not_instance(value: object, comparable: type) -> bool:
    """
    Checks whether `value` is not an instance of `comparable`.
    """

    return not isinstance(value, comparable)
