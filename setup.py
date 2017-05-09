# coding=utf-8
from distutils.core import setup
from setuptools import find_packages

__author__ = "Gareth Coles"


setup(
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
    namespace_packages=["ultros", "ultros.networks", "ultros.plugins"]
)
