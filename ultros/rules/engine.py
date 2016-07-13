# coding=utf-8

"""
A basic rules engine, included so plugins and other things don't have to write
their own. It's not *extremely* flexible, but it should cover
most use-cases.
"""

import types

from asyncio.coroutines import iscoroutinefunction
from typing import Union

from ultros.rules.constants import TransformerResult

__author__ = 'Gareth Coles'


class RulesEngine:
    """
    The Ultros rules engine. Define sets of rules, including what happens
    when each rule is matched, and use them to compare values as they
    come.

    This engine does have the concept of sets of rules, so you can use the
    same instance with more than one group of rules.
    """
    
    # TODO: Value-editing transformers

    predicates = {}
    rule_sets = {}

    async def run(self, rule_set: str, value: object) -> object:
        """
        Run a set of rules against a value, returning as required by your
        transformers. It follows these basic steps:

        * Iterate over the rules in the set. For each rule:

            * Check the predicate against the comparable in the rule and the
              given value

                * If the predicate returns True, run the transformer
                * If the transformer returns CONTINUE, move on to the next rule
                * If the transformer returns STOP, return None and stop
                  processing
                * If the transformer returns a tuple and the first value is
                  STOP, return the second value

            * If the predicate returns False, return False and stop processing

        :param rule_set: The set of rules to run
        :param value: The value you want to compare across your rules
        :return: What you get depends entirely on your rules; see above
        """

        _set = self.get_rule_set(rule_set)

        if _set is None:
            raise LookupError("No such rule set: {}".format(rule_set))

        for predicate, comparable, transformer in _set:
            if iscoroutinefunction(predicate):
                result = await predicate(value, comparable)
            else:
                result = predicate(value, comparable)

            if result:
                if iscoroutinefunction(transformer):
                    transformer_result = await transformer(value)
                else:
                    transformer_result = transformer(value)
            else:
                return False  # Rule wasn't matched

            if isinstance(transformer_result, tuple):
                # Updates the value being compared above
                t_r, value = transformer_result

                if t_r is TransformerResult.CONTINUE:
                    continue  # Continues with the updated value
                if t_r is TransformerResult.RETURN:
                    return value

            if transformer_result is TransformerResult.CONTINUE:
                continue
            if transformer_result is TransformerResult.RETURN:
                return

            raise NotImplementedError(
                "Unknown transformer result: {}".format(transformer_result)
            )

    def add_rule(self,
                 rule_set: str,
                 predicate: Union[types.FunctionType, types.CoroutineType],
                 comparable: object,
                 transformer: Union[types.FunctionType, types.CoroutineType]):
        """
        Add a rule to a rule set. If the set doesn't exist, it is created.

        :param rule_set: The rule set to add the rule to
        :param predicate: A function representing a simple two-value comparison
        :param comparable: The right-side value to compare with every time this
                           rule is encountered
        :param transformer: The transformer function to run and check if the
                            rule is matched
        """

        if rule_set not in self.rule_sets:
            self.rule_sets[rule_set] = []

        self.rule_sets[rule_set].append(
            (predicate, comparable, transformer)
        )

    def get_rule_set(self, rule_set: str) -> list:
        """
        Get a set of rules, as defined.

        :param rule_set: The rule set to get
        :return: The rule set, or None if it doesn't exist
        """

        return self.rule_sets.get(rule_set, None)

    def del_rule_set(self, rule_set: str):
        """
        Delete a rule set, assuming it exists.

        :param rule_set: The rule set to delete
        """

        if rule_set in self.rule_sets:
            del self.rule_sets[rule_set]
