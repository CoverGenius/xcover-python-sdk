# -*- coding: utf-8 -*-

"""
Registry package for the xCover-Library.
This package allows the user of the package to change the classes and functions
used in xcoverlib, so that he can easily change the implementations used in various
parts.
"""

from .registry import _Registry
registry = _Registry()
