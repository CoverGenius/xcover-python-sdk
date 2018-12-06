# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='xcovlib',
    version='0.5.0',
    description='XCover API client library for Python',
    long_description=readme,
    author='Udit Agarwal',
    author_email='udit@covergenius.biz',
    url='https://github.com/CoverGenius/xcover-python-sdk/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['pycryptodome==3.7.2', 'httpsig', 'requests'],  # external packages as dependencies
)

