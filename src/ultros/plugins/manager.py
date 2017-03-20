# coding=utf-8
from ultros import ultros as u

__author__ = "Gareth Coles"


class PluginManager:
    ultros = None

    def __init__(self, ultros: u.Ultros):
        self.ultros = ultros

    def shutdown(self):
        self.ultros = None
