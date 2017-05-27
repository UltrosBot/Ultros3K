# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true
from unittest import TestCase

from ultros.core.storage.data.yaml import YAMLData
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestYAML(TestCase):
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

        shutil.copy(os.path.join(tests_dir, "files/test.yml"), os.path.join(self.data_dir, "test.yml"))

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
        YAML data testing: Dict functionality
        """

        def _data_object() -> YAMLData:
            return self.manager.get_data(
                "test.yml", None
            )

        data_obj = _data_object()

        data_obj.clear()

        assert_equal(
            len(data_obj),
            0
        )

        data_obj.reload()

        assert_equal(
            len(data_obj),
            6
        )

        assert_equal(
            data_obj.copy(),
            data_obj.data
        )

        assert_equal(
            data_obj.get("test"),
            "test"
        )

        assert_equal(
            list(data_obj.items()),
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
            list(data_obj.keys()),
            ["test", "herp", "int", "float", "boolean", "other_boolean"]
        )

        assert_equal(
            data_obj.pop("test"),
            "test"
        )

        assert_equal(
            list(data_obj.keys()),
            ["herp", "int", "float", "boolean", "other_boolean"]
        )

        data_obj.reload()
        data_obj.popitem()

        assert_equal(
            len(data_obj),
            5
        )

        data_obj.reload()

        assert_equal(
            data_obj.setdefault("berp", "lerp"),
            "lerp"
        )

        assert_equal(
            data_obj.get("berp"),
            "lerp"
        )

        data_obj.reload()
        data_obj.update({"berp": "lerp"})

        assert_equal(
            data_obj.get("berp"),
            "lerp"
        )

        data_obj.reload()

        assert_equal(
            list(data_obj.values()),
            ["test", "derp", 1, 1.1, True, False]
        )

        assert_true(
            "test" in data_obj
        )

        del data_obj["test"]

        assert_true(
            "test" not in data_obj
        )

        data_obj.reload()

        assert_equal(
            data_obj["test"],
            "test"
        )

        assert_equal(
            list(data_obj),
            ["test", "herp", "int", "float", "boolean", "other_boolean"]
        )

        assert_equal(
            len(data_obj),
            6
        )

        data_obj["x"] = "y"

        assert_equal(
            data_obj["x"],
            "y"
        )

    def test_read(self):
        """
        YAML data testing: Reading
        """

        def _data_object() -> YAMLData:
            return self.manager.get_data(
                "test.yml", None
            )

        data_obj = _data_object()

        assert_equal(
            data_obj["test"],
            "test"
        )

        assert_equal(
            data_obj["herp"],
            "derp"
        )

        assert_equal(
            data_obj["int"],
            1
        )

        assert_equal(
            data_obj["float"],
            1.1
        )

        assert_equal(
            data_obj["boolean"],
            True
        )

        assert_equal(
            data_obj["other_boolean"],
            False
        )

    def test_write(self):
        """
        YAML data testing: Writing
        """

        def _data_object() -> YAMLData:
            return self.manager.get_data(
                "test.yml", None
            )

        data_obj = _data_object()

        with data_obj:
            data_obj["test"] = "test2"
            data_obj["int"] = 2
            data_obj["float"] = 2.2
            data_obj["boolean"] = False
            data_obj["other_boolean"] = True
            data_obj["list"] = ["herp"]
            data_obj["dict"] = {"herp": "derp"}

        data_obj.reload()

        assert_equal(
            data_obj["test"],
            "test2"
        )

        assert_equal(
            data_obj["int"],
            2
        )

        assert_equal(
            data_obj["float"],
            2.2
        )

        assert_equal(
            data_obj["boolean"],
            False
        )

        assert_equal(
            data_obj["other_boolean"],
            True
        )

        assert_equal(
            data_obj["list"],
            ["herp"]
        )

        assert_equal(
            data_obj["dict"],
            {"herp": "derp"}
        )
