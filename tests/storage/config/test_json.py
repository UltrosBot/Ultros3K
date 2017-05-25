# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase

from ultros.core.storage.config.json import JSONConfig
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestJSON(TestCase):
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

        shutil.copy(os.path.join(tests_dir, "files/test.json"), os.path.join(self.config_dir, "test.json"))

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
        JSON config testing: Dict functionality
        """

        def _config_object() -> JSONConfig:
            return self.manager.get_config(
                "test.json", None
            )

        config_obj = _config_object()

        config_obj.clear()

        assert_equal(
            len(config_obj),
            0
        )

        config_obj.reload()

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
            config_obj.pop("test"),
            "test"
        )

        assert_equal(
            list(config_obj.keys()),
            ["herp", "int", "float", "boolean", "other_boolean"]
        )

        config_obj.reload()
        config_obj.popitem()

        assert_equal(
            len(config_obj),
            5
        )

        config_obj.reload()

        assert_equal(
            config_obj.setdefault("berp", "lerp"),
            "lerp"
        )

        assert_equal(
            config_obj.get("berp"),
            "lerp"
        )

        config_obj.reload()
        config_obj.update({"berp": "lerp"})

        assert_equal(
            config_obj.get("berp"),
            "lerp"
        )

        config_obj.reload()

        assert_equal(
            list(config_obj.values()),
            ["test", "derp", 1, 1.1, True, False]
        )

        assert_true(
            "test" in config_obj
        )

        del config_obj["test"]

        assert_true(
            "test" not in config_obj
        )

        config_obj.reload()

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

        config_obj["x"] = "y"

        assert_equal(
            config_obj["x"],
            "y"
        )

    def test_read(self):
        """
        JSON config testing: Reading
        """

        def _config_object() -> JSONConfig:
            return self.manager.get_config(
                "test.json", None
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

    def test_write(self):
        """
        JSON config testing: Writing
        """

        def _config_object() -> JSONConfig:
            return self.manager.get_config(
                "test.json", None
            )

        config_obj = _config_object()

        with config_obj:
            config_obj["test"] = "test2"
            config_obj["int"] = 2
            config_obj["float"] = 2.2
            config_obj["boolean"] = False
            config_obj["other_boolean"] = True
            config_obj["list"] = ["herp"]
            config_obj["dict"] = {"herp": "derp"}

        config_obj.reload()

        assert_equal(
            config_obj["test"],
            "test2"
        )

        assert_equal(
            config_obj["int"],
            2
        )

        assert_equal(
            config_obj["float"],
            2.2
        )

        assert_equal(
            config_obj["boolean"],
            False
        )

        assert_equal(
            config_obj["other_boolean"],
            True
        )

        assert_equal(
            config_obj["list"],
            ["herp"]
        )

        assert_equal(
            config_obj["dict"],
            {"herp": "derp"}
        )
