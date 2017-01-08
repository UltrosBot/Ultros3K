# coding=utf-8
from distutils.core import setup

__author__ = "Gareth Coles"


setup(
    name='Ultros',
    version='0.0.1',
    author='Gareth Coles',
    author_email='gdude2002@gmail.com',
    packages=['ultros'],
    url='http://pypi.python.org/pypi/Ultros/',
    license='LICENSE.txt',
    description='The only squid that connects communities!',
    long_description=open('README.txt').read(),
    install_requires=open(
        "requirements.txt"
    ).read().replace("\r", "").split("\n"),
)
