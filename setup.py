# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='xcovlib',
    version='0.1.0',
    description='SDK to Connect to xCover core',
    long_description=readme,
    author='xCover Team',
    author_email='python+devs@covergenius.biz',
    url='https://github.com/sample/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

