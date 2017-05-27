# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase

from ultros.core.storage.data.ini import INIData
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

        shutil.copy(os.path.join(tests_dir, "files/test.ini"), os.path.join(self.data_dir, "test.ini"))

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

    def test_read(self):
        """
        INI data testing (Reading)
        """

        def _data_object() -> INIData:
            return self.manager.get_data(
                "test.ini", None
            )

        data_obj = _data_object()

        sections = data_obj.sections()
        options = data_obj.options("Test")

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
            data_obj.items("Test"),
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
            dict(data_obj.items("Test")),
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
            data_obj.get("Test", "test"),
            "test"
        )

        assert_equal(
            data_obj.get_int("Test", "int"),
            1
        )

        assert_equal(
            data_obj.get_float("Test", "float"),
            1.1
        )

        assert_equal(
            data_obj.get_boolean("Test", "boolean"),
            True
        )

        assert_equal(
            data_obj.get_boolean("Test", "other_boolean"),
            False
        )

        with assert_raises(ValueError):
            data_obj.get_int("Test", "herp")

        with assert_raises(ValueError):
            data_obj.get_float("Test", "herp")

        with assert_raises(ValueError):
            data_obj.get_boolean("Test", "herp")

        assert_equal(
            data_obj["Test":"herp"],
            "derp"
        )

        assert_equal(
            data_obj["Test"]["herp"],
            "derp"
        )

        assert_true(
            "Test" in data_obj
        )

        assert_equal(
            len(data_obj),
            2  # Default section is always counted whether it exists or not
        )

    def test_write(self):
        """
        INI data testing (Writing)
        """

        def _data_object() -> INIData:
            return self.manager.get_data(
                "test.ini", None
            )

        data_obj = _data_object()

        data_obj.add_section("Data")
        data_obj.set("Data", "x", "y")

        data_obj.save()
        data_obj.reload()

        assert_true(
            data_obj.has_section("Data")
        )

        assert_equal(
            data_obj.get("Data", "x"),
            "y"
        )

        data_obj.remove_section("Data")
        data_obj.save()
        data_obj.reload()

        assert_true(
            not data_obj.has_section("Data")
        )

        with assert_raises(TypeError):
            data_obj["Data"] = 123213

        with assert_raises(TypeError):
            data_obj[2] = 3

        data_obj["Data"] = {
            "x": "y",
            "a": "b"
        }

        data_obj["Data":"c"] = "d"

        data_obj.save()
        data_obj.reload()

        assert_true(
            data_obj.has_section("Data")
        )

        assert_equal(
            data_obj.get("Data", "x"),
            "y"
        )

        assert_equal(
            data_obj.get("Data", "a"),
            "b"
        )

        assert_equal(
            data_obj.get("Data", "c"),
            "d"
        )

        del data_obj["Data":"c"]

        assert_true(
            not data_obj.has_option("Data", "c")
        )

        del data_obj["Data"]

        assert_true(
            not data_obj.has_section("Data")
        )
