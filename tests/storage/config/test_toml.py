# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true
from unittest import TestCase

from ultros.core.storage.config.toml import TOMLConfig
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestTOML(TestCase):
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

        shutil.copy(os.path.join(tests_dir, "files/test.toml"), os.path.join(self.config_dir, "test.toml"))

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

    def test_dict_functionality(self):
        """
        TOML config testing: Dict functionality
        """

        def _config_object() -> TOMLConfig:
            return self.manager.get_config(
                "test.toml", None
            )

        config_obj = _config_object()

        assert_equal(
            len(config_obj),
            6
        )

        assert_equal(
            config_obj.copy(),
            config_obj.data
        )

        assert_equal(
            config_obj.get("test"),
            "test"
        )

        assert_equal(
            list(config_obj.items()),
            [
                ("test", "test"),
                ("herp", "derp"),
                ("int", 1),
                ("float", 1.1),
                ("boolean", True),
                ("other_boolean", False)
            ]
        )

        assert_equal(
            list(config_obj.keys()),
            ["test", "herp", "int", "float", "boolean", "other_boolean"]
        )

        assert_equal(
            list(config_obj.values()),
            ["test", "derp", 1, 1.1, True, False]
        )

        assert_true(
            "test" in config_obj
        )

        assert_equal(
            config_obj["test"],
            "test"
        )

        assert_equal(
            list(config_obj),
            ["test", "herp", "int", "float", "boolean", "other_boolean"]
        )

        assert_equal(
            len(config_obj),
            6
        )

    def test_read(self):
        """
        TOML config testing: Reading
        """

        def _config_object() -> TOMLConfig:
            return self.manager.get_config(
                "test.toml", None
            )

        config_obj = _config_object()

        assert_equal(
            config_obj["test"],
            "test"
        )

        assert_equal(
            config_obj["herp"],
            "derp"
        )

        assert_equal(
            config_obj["int"],
            1
        )

        assert_equal(
            config_obj["float"],
            1.1
        )

        assert_equal(
            config_obj["boolean"],
            True
        )

        assert_equal(
            config_obj["other_boolean"],
            False
        )
