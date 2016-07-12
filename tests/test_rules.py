# coding=utf-8
import asyncio

import ultros.rules.predicates as p
import ultros.rules.transformers as t

from ultros.rules.engine import RulesEngine
from ultros.rules.constants import TransformerResult

from nose.tools import assert_equal, assert_true
from unittest import TestCase


__author__ = 'Gareth Coles'


class TestRules(TestCase):
    def setUp(self):
        self.engine = RulesEngine()
        self.rule_set = ""
        self.value = ""

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        del self.engine
        del self.loop
        del self.rule_set
        del self.value

    async def do_run(self):
        return await self.engine.run(self.rule_set, self.value)

    def test_basics(self):
        """
        Rules engine basics
        """

        def predicate_true(*args):
            return True

        def predicate_false(*args):
            return False

        def transformer_continue():
            return TransformerResult.CONTINUE

        def transformer_return():
            return TransformerResult.RETURN

        def transformer_return_value(value):
            def inner():
                return TransformerResult.RETURN, value
            return inner

        self.engine.add_rule(
            "Test1", predicate_true, "", transformer_return_value("a")
        )
        self.engine.add_rule(
            "Test2", predicate_false, "", transformer_continue
        )
        self.engine.add_rule(
            "Test2", predicate_true, "", transformer_return_value("a")
        )
        self.engine.add_rule(
            "Test3", predicate_true, "", transformer_continue
        )
        self.engine.add_rule(
            "Test3", predicate_true, "", transformer_return
        )

        self.rule_set = "Test1"
        self.value = ""

        result = self.loop.run_until_complete(self.do_run())
        assert_equal(
            result,
            "a",
            "Invalid result for Test1; expected \"a\", got {}".format(
                repr(result)
            )
        )

        self.rule_set = "Test2"

        result = self.loop.run_until_complete(self.do_run())
        assert_equal(
            result,
            False,
            "Invalid result for Test2; expected False, got {}".format(
                repr(result)
            )
        )

        self.rule_set = "Test3"

        result = self.loop.run_until_complete(self.do_run())
        assert_equal(
            result,
            None,
            "Invalid result for Test3; expected None, got {}".format(
                repr(result)
            )
        )

    def test_predicates(self):
        """
        Bundled predicates
        """

        def transformer_return_value(value):
            def inner():
                return TransformerResult.RETURN, value
            return inner

        self.engine.add_rule(
            "x > y",
            p.num_greater_than, 5, transformer_return_value(True)
        )

        self.rule_set = "x > y"
        self.value = 10
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x > y")

        self.engine.add_rule(
            "x < y",
            p.num_less_than, 5, transformer_return_value(True)
        )

        self.rule_set = "x < y"
        self.value = 0
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x < y")

        self.engine.add_rule(
            "x contains y",
            p.str_contains, "abcd", transformer_return_value(True)
        )

        self.rule_set = "x contains y"
        self.value = "a"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x contains y")

        self.engine.add_rule(
            "x matches y",
            p.str_matches_regex, r"[a]+", transformer_return_value(True)
        )

        self.rule_set = "x matches y"
        self.value = "aaaa"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x matches y")

        self.engine.add_rule(
            "x not contains y",
            p.str_not_contains, "bbbb", transformer_return_value(True)
        )

        self.rule_set = "x not contains y"
        self.value = "a"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: not x contains y")

        self.engine.add_rule(
            "x not matches y",
            p.str_not_matches_regex, r"[a]+", transformer_return_value(True)
        )

        self.rule_set = "x not matches y"
        self.value = "bbbb"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: not x matches y")

        self.engine.add_rule(
            "x == y",
            p.equal, 5, transformer_return_value(True)
        )

        self.rule_set = "x == y"
        self.value = 5
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x == y")

        identical_object = object()
        non_identical_object = object()

        self.engine.add_rule(
            "x is y",
            p.identical, identical_object, transformer_return_value(True)
        )

        self.rule_set = "x is y"
        self.value = identical_object
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x is y")

        self.engine.add_rule(
            "x != y",
            p.not_equal, 5, transformer_return_value(True)
        )

        self.rule_set = "x != y"
        self.value = 10
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x != y")

        self.engine.add_rule(
            "x is not y",
            p.not_identical, identical_object, transformer_return_value(True)
        )

        self.rule_set = "x is not y"
        self.value = non_identical_object
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x is not y")

        self.engine.add_rule(
            "x isinstance y",
            p.is_instance, str, transformer_return_value(True)
        )

        self.rule_set = "x isinstance y"
        self.value = "abcd"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: x isinstance y")

        self.engine.add_rule(
            "x not isinstance y",
            p.is_not_instance, int, transformer_return_value(True)
        )

        self.rule_set = "x not isinstance y"
        self.value = "abcd"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "FALSE: not x isinstance y")

    def test_transformers(self):
        """
        Bundled transformers
        """

        def predicate_true(*args):
            return True

        def return_true():
            return True

        self.engine.add_rule(
            "stop", predicate_true, "", t.trans_stop
        )

        self.rule_set = "stop"
        result = self.loop.run_until_complete(self.do_run())
        assert_equal(result, None, "Failed: trans_stop")

        self.engine.add_rule(
            "factory_return", predicate_true, "", t.factory_trans_return(True)
        )

        self.rule_set = "factory_return"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: factory_trans_return")

        self.engine.add_rule(
            "factory_return_call", predicate_true, "",
            t.factory_trans_return_call(return_true)
        )

        self.rule_set = "factory_return_call"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: factory_return_call")

        self.engine.add_rule(
            "continue", predicate_true, "", t.trans_continue
        )
        self.engine.add_rule(
            "continue", predicate_true, "", t.factory_trans_return(True)
        )

        self.rule_set = "continue"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: trans_continue")
