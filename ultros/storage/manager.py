# coding=utf-8

import os

__author__ = 'Gareth Coles'


class StorageManager:
    config_location = None
    data_location = None

    data_files = None
    config_files = None
    databases = None

    def __init__(self, config_location, data_location):
        self.config_location = os.path.normpath(config_location)
        self.data_location = os.path.normpath(data_location)

        self.data_files = {}
        self.config_files = {}
        self.databases = {}

    def get_data(self):
        pass

    def get_config(self):
        pass

    def get_database(self):
        pass
