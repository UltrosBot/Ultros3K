# coding=utf-8

"""
A basic rules engine, as well as a set of standard predicates and transformers.

* Predicates are the equivalent of a conditional. They take the comparable
  given in the rule on the left and compare it to the value being tested
  on the right, returning a boolean.
* Transformers can be considered a form of result. If a rule is matched, the
  transformer is run.

See each module below for more information on how everything works.

Submodules
==========

.. currentmodule:: ultros.rules

.. autosummary::
    :toctree: rules

    constants
    engine
    predicates
    transformers
"""

__author__ = 'Gareth Coles'
