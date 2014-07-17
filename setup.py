#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from connection import __version__, __author__, __contact__

# use requirements.txt for dependencies
#with open('requirements.txt') as f:
#    required = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='connection',
    version=__version__,
    description='Connector to other sites',
    long_description=readme,
    author=__author__,
    author_email=__contact__,
    url='https://github.com/kartikprabhu/connection',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
