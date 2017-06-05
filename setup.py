# coding=utf-8
import os
import shutil
from distutils.command.install import INSTALL_SCHEMES

from setuptools import find_packages, setup, Command
from setuptools.command.build_py import build_py

__author__ = "Gareth Coles"


class BuildZipsCommand(Command):
    """
    A custom command to build a zip of config files needed for initial installs
    """

    description = "Build zip of bundled config files"

    def run(self):
        if os.path.exists("files.zip"):
            print("Removing old 'files.zip'")
            os.remove("files.zip")

        shutil.make_archive("files", "zip", "bundled_files/")
        print("bundled_files/ -> files.zip")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class BuildPyCommand(build_py):
    """
    Custom build command that calls the zip-building command
    """

    def run(self):
        self.run_command("build_zip")
        build_py.run(self)

for scheme in INSTALL_SCHEMES.values():
    scheme["data"] = scheme["purelib"]

setup(
    cmdclass={
        "build_zip": BuildZipsCommand,
        "build_py": BuildPyCommand
    },

    name='Ultros',
    version='0.0.1',
    author='Gareth Coles, Sean Gordon',
    author_email='Gareth Coles <gdude2002@gmail.com>',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://pypi.python.org/pypi/Ultros/',
    license='LICENSE.txt',
    description='The only squid that connects communities!',
    long_description=open('README.txt').read(),
    install_requires=open(
        "requirements.txt"
    ).read().replace("\r", "").split("\n"),
    extras_require={"uvloop": "uvloop"},
    namespace_packages=["ultros", "ultros.networks", "ultros.plugins"],
    data_files=[("", ["files.zip"])]
)
