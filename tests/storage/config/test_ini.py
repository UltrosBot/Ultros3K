# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase

from ultros.core.storage.config.ini import INIConfig
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestINI(TestCase):
    def setUp(self):
        self.directory = os.path.join(tempfile.gettempdir(), secrets.token_urlsafe(10))

        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        self.config_dir = os.path.join(self.directory, "config")
        self.data_dir = os.path.join(self.directory, "data")

        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        current_dir = os.path.dirname(__file__)
        tests_dir = os.path.join(current_dir, "../../")

        shutil.copy(os.path.join(tests_dir, "files/test.ini"), os.path.join(self.config_dir, "test.ini"))

        self.manager = StorageManager(
            ultros=None,
            config_location=self.config_dir,
            data_location=self.data_dir
        )

    def tearDown(self):
        self.manager.shutdown()
        del self.manager

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

    def test_ini(self):
        """
        INI config testing
        """

        def _config_object() -> INIConfig:
            return self.manager.get_config(
                "test.ini", None
            )

        config_obj = _config_object()

        sections = config_obj.sections()
        options = config_obj.options("Test")

        assert_equal(
            sections,
            ["Test"],
            "Expected a single Test section, got {}".format(sections)
        )

        assert_equal(
            options,
            ["test", "herp", "int", "float", "boolean", "other_boolean"],
            "Expected the following options: ['test', 'herp', 'int', 'float', 'boolean', 'other_boolean'], got {}".format(options)
        )

        assert_equal(
            config_obj.items("Test"),
            [
                ("test", "test"), 
                ("herp", "derp"),

                ("int", "1"),
                ("float", "1.1"),
                ("boolean", "true"),
                ("other_boolean", "false"),
            ]
        )

        assert_equal(
            dict(config_obj.items("Test")),
            {
                "test": "test",
                "herp": "derp",

                "int": "1",
                "float": "1.1",
                "boolean": "true",
                "other_boolean": "false"
            }
        )

        assert_equal(
            config_obj.get("Test", "test"),
            "test"
        )

        assert_equal(
            config_obj.get_int("Test", "int"),
            1
        )

        assert_equal(
            config_obj.get_float("Test", "float"),
            1.1
        )

        assert_equal(
            config_obj.get_boolean("Test", "boolean"),
            True
        )

        assert_equal(
            config_obj.get_boolean("Test", "other_boolean"),
            False
        )

        with assert_raises(ValueError):
            config_obj.get_int("Test", "herp")

        with assert_raises(ValueError):
            config_obj.get_float("Test", "herp")

        with assert_raises(ValueError):
            config_obj.get_boolean("Test", "herp")

        assert_equal(
            config_obj["Test":"herp"],
            "derp"
        )

        assert_equal(
            config_obj["Test"]["herp"],
            "derp"
        )

        assert_true(
            "Test" in config_obj
        )

        assert_equal(
            len(config_obj),
            2  # Default section is always counted whether it exists or not
        )
