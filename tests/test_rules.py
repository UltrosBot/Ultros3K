# coding=utf-8
import asyncio

import ultros.core.rules.predicates as p
import ultros.core.rules.transformers as t

from ultros.core.rules.engine import RulesEngine
from ultros.core.rules.constants import TransformerResult

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase


__author__ = "Gareth Coles"


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

        def predicate_is_true(value, comparable):
            return value is True

        def transformer_continue(value):
            return TransformerResult.CONTINUE

        def transformer_continue_value(_value):
            def inner(value):
                return TransformerResult.CONTINUE, _value
            return inner

        def transformer_return(value):
            return TransformerResult.RETURN

        def transformer_return_value(_value):
            def inner(value):
                return TransformerResult.RETURN, _value
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

        self.engine.add_rule(
            "Test4", predicate_true, "", transformer_continue_value(True)
        )
        self.engine.add_rule(
            "Test4", predicate_is_true, "", transformer_return_value(True)
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

        self.rule_set = "Test4"

        result = self.loop.run_until_complete(self.do_run())
        assert_equal(
            result,
            True,
            "Invalid result for Test4; expected True, got {}".format(
                repr(result)
            )
        )

    def test_predicates(self):
        """
        Bundled predicates
        """

        def transformer_return_value(value):
            def inner(_value):
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

        def predicate_is_true(value, comparable):
            return value is True

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

        self.engine.add_rule(
            "factory_trans_continue", predicate_true, "",
            t.factory_trans_continue(True)
        )
        self.engine.add_rule(
            "factory_trans_continue", predicate_is_true, "",
            t.factory_trans_return(True)
        )

        self.rule_set = "factory_trans_continue"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: factory_trans_continue")

        self.engine.add_rule(
            "factory_trans_continue_call", predicate_true, "",
            t.factory_trans_continue_call(lambda *_, **__: True)
        )
        self.engine.add_rule(
            "factory_trans_continue_call", predicate_is_true, "",
            t.factory_trans_return(True)
        )

        self.rule_set = "factory_trans_continue_call"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: factory_trans_continue_call")

    def test_edge_cases(self):
        self.engine.add_rule(
            "Test1", p.equal, "", t.factory_trans_return(True)
        )

        self.engine.del_rule_set("Test1")

        self.rule_set = "Test1"
        assert_raises(LookupError, self.loop.run_until_complete, self.do_run())

        def predicate_true(*args):
            return True

        self.engine.add_rule(
            "Test2", predicate_true, "", lambda *_, **__: "derp"
        )

        self.rule_set = "Test2"

        assert_raises(
            NotImplementedError, self.loop.run_until_complete, self.do_run()
        )

        async def async_predicate_true(value, comparable):
            return True

        async def async_transformer_return_true(value):
            return TransformerResult.RETURN, True

        self.engine.add_rule(
            "Test3", async_predicate_true, "", async_transformer_return_true
        )

        self.rule_set = "Test3"
        result = self.loop.run_until_complete(self.do_run())
        assert_true(result, "Failed: Test3")
