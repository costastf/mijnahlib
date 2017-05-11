#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: mijnahlib.py
"""
Main module file

Put your classes here
"""

import logging
from requests import Session
from bs4 import BeautifulSoup as Bfs

from .mijnahlibexceptions import InvalidCredentials, UnknownServerError

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''10-05-2017'''

# This is the main prefix used for logging
LOGGER_BASENAME = '''mijnahlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

LOGIN_ERROR_MESSAGE = 'Het e-mailadres en/of wachtwoord is onjuist'


class Server(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._session = Session()
        self._url = 'https://www.ah.nl'
        self._authenticate()
        self.shopping_cart = ShoppingCart(self)

    def _authenticate(self):
        data = {'userName': self.username,
                'password': self.password,
                'rememberUser': True}
        url = '{base}/mijn/inloggen/basis'.format(base=self._url)
        response = self._session.post(url, data=data)
        # at this point we don't have enough information to know what went
        # wrong if we didn't get a valid response.
        if not response.ok:
            raise UnknownServerError(response.text)
        soup = Bfs(response.text, 'html.parser')
        # we did not login successfully
        if LOGIN_ERROR_MESSAGE in response.text:
            error = soup.find('div', {'class': 'error_notices'}).text
            raise InvalidCredentials(error)
        # we try to get the redirect we are provided with in the meta tag
        redirect = soup.find('meta').attrs['content'].split('=')[1]
        success_url = '{base}{redirect}'.format(base=self._url,
                                                redirect=redirect)
        self._session.get(success_url)
        return True


class ShoppingCart(object):
    def __init__(self, ah_instance):
        self._ah = ah_instance
        self._url = ('{base}/service/rest/shoppinglists/0/'
                     'items').format(base=self._ah._url)

    def add_item_by_id(self, item_id, quantity=1):
        data = {'type': 'PRODUCT',
                'item': {'id': item_id},
                'quantity': int(quantity)}
        response = self._ah._session.post(self._url, json=data)
        if response.ok:
            return True
        else:
            return False

    @property
    def contents(self):
        url = ('{base}/service/rest/delegate'
               '?url=%2Fmijnlijst').format(base=self._ah._url)
        response = self._ah._session.get(url)
        data = response.json()
        items_lane = next((lane for lane in data['_embedded']['lanes']
                           if lane['type'] == 'ShoppingListLane'), None)
        return items_lane['_embedded']['items']
