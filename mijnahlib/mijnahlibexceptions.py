#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: mijnahlibexceptions.py
#
"""
Main module Exceptions file

Put your exception classes here
"""

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''10-05-2017'''


class UnknownServerError(Exception):
    """Server did not respond as expected"""


class InvalidCredentials(Exception):
    """Username and password combination is invalid"""
