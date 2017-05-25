# coding=utf-8
import os
import secrets
import shutil
import tempfile

from nose.tools import assert_equal, assert_true, assert_raises
from unittest import TestCase

from ultros.core.storage.formats import INI
from ultros.core.storage.manager import StorageManager


__author__ = "Gareth Coles"


class TestManager(TestCase):
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
        tests_dir = os.path.join(current_dir, "../")

        shutil.copy(os.path.join(tests_dir, "files/test.ini"), os.path.join(self.config_dir, "test.ini"))
        shutil.copy(os.path.join(tests_dir, "files/test.ini"), os.path.join(self.config_dir, "test2.ini.default"))
        shutil.copy(os.path.join(tests_dir, "files/test.json"), os.path.join(self.config_dir, "test.json.default"))

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

    def test_basics(self):
        """
        Storage manager basics
        """
        from ultros.core.storage.config.ini import INIConfig

        result = self.manager.file_formats.get_format_from_path("test.ini")

        assert_equal(
            result,
            self.manager.file_formats._extensions[INI],
            "Invalid format for test.ini; expected {}, got {}".format(
                repr(self.manager.file_formats._extensions[INI]), repr(result)
            )
        )

        result = self.manager.get_class(result.config)

        assert_equal(
            result,
            INIConfig,
            "Invalid class for INI format; expected {}, got {}".format(
                repr(INIConfig), repr(result)
            )
        )

        config_obj = self.manager.get_config(
            "test.ini", None
        )

        assert_true(
            isinstance(config_obj, INIConfig),
            "INI config object {} is not an instance of INIConfig".format(repr(config_obj))
        )

        default_config_obj = self.manager.get_config(
            "test2.ini", None
        )

        assert_true(
            isinstance(default_config_obj, INIConfig),
            "INI config object {} is not an instance of {}".format(
                repr(default_config_obj), repr(INIConfig)
            )
        )

        default_path = os.path.join(self.config_dir, "test2.ini.default")

        assert_equal(
            default_config_obj.path,
            default_path,
            "Default config object has the wrong path; expected {}, got {}".format(
                default_path, default_config_obj.path
            )
        )

        default_json_config_obj = self.manager.get_config(
            "test.json", None
        )

        with assert_raises(RuntimeError):
            default_json_config_obj.save()

        with assert_raises(FileNotFoundError):
            self.manager.get_config(
                "test2.ini", None, defaults_path=False
            )
