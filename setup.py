#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# use requirements.txt for dependencies
with open('requirements.txt') as f:
    required = map(lambda s: s.strip(), f.readlines())

with open('requirements-links.txt') as f:
    required_links = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='connection',
    version='0.2.0',
    description='Connector to other sites',
    long_description=readme,
	install_requires=required,
	dependency_links=required_links,
    author='Kartik Prabhu',
    author_email='me@kartikprabhu.com',
    url='https://github.com/kartikprabhu/connection',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
