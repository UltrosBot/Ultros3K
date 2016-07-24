# coding=utf-8

"""
A module for a predefined set of basic transformers.

A transformer is a result - It tells the rules engine what to do when a
rule is matched. As a result, they must return one of the following:

* TransformerResult.CONTINUE - Meaning, "Continue with the next rule"
* TransformerResult.RETURN - Meaning, "Stop processing"
* A tuple containing the following:

    * Index 0: TransformerResult.RETURN ("Stop processing, and...")
    * Index 1: Some value ("...return this value")

* A tuple containing the following:

    * Index 0: TransformerResult.CONTINUE ("continue processing, but...")
    * Index 1: Some value ("...use this value instead")

If your transformer doesn't return one of those, the rules engine will raise a
NotImplementedError. Note that transformers may either be a standard function,
or a coroutine function.
"""

import types

from ultros.rules.constants import TransformerResult

__author__ = "Gareth Coles"


def trans_continue(value) -> TransformerResult:
    """
    A transformer that simply returns TransformerResult.CONTINUE.
    """

    return TransformerResult.CONTINUE


def trans_stop(value) -> TransformerResult:
    """
    A transformer that simply returns TransformerResult.RETURN.
    """

    return TransformerResult.RETURN


def factory_trans_return(_value) -> types.FunctionType:
    """
    A factory function that produces a transformer which returns
    TransformerResult.RETURN along with a given value.

    :param _value: The value to return with the result
    """

    def inner(value) -> (TransformerResult, object):
        return TransformerResult.RETURN, _value
    return inner


def factory_trans_return_call(func: types.FunctionType,
                              *args, **kwargs) -> types.FunctionType:
    """
    A factory function that produces a transformer which returns
    TransformerResult.RETURN along with the result of a callable function.

    :param func: The function to call when this transformer is reached
    :param args: Positional arguments to pass to the function
    :param kwargs: Keyword arguments to pass to the function
    """

    def inner(value) -> (TransformerResult, object):
        return TransformerResult.RETURN, func(*args, **kwargs)
    return inner


def factory_trans_continue(_value) -> types.FunctionType:
    """
    A factory function that produces a transformer which returns
    TransformerResult.CONTINUE along with a given value.

    :param _value: The value to return with the result
    """

    def inner(value) -> (TransformerResult, object):
        return TransformerResult.CONTINUE, _value
    return inner


def factory_trans_continue_call(func: types.FunctionType,
                                *args, **kwargs) -> types.FunctionType:
    """
    A factory function that produces a transformer which returns
    TransformerResult.CONTINUE along with the result of a callable function.

    :param func: The function to call when this transformer is reached
    :param args: Positional arguments to pass to the function
    :param kwargs: Keyword arguments to pass to the function
    """

    def inner(value) -> (TransformerResult, object):
        return TransformerResult.CONTINUE, func(*args, **kwargs)
    return inner
