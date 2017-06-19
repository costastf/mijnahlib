# -*- coding: utf-8 -*-
"""
mijnahlib package

Imports all parts from mijnahlib here
"""
from ._version import __version__
from .mijnahlibexceptions import (InvalidCredentials,
                                  UnknownServerError,
                                  NoAuthRedirect)

from .mijnahlib import Server

__author__ = '''Costas Tyfoxylos'''
__email__ = '''costas.tyf@gmail.com'''

# This is to 'use' the module(s), so lint doesn't complain
assert __version__

# assert exception
assert InvalidCredentials
assert UnknownServerError
assert NoAuthRedirect

# assert objects
assert Server
