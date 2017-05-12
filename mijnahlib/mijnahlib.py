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
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                               suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self.username = username
        self.password = password
        self.session = Session()
        self.url = 'https://www.ah.nl'
        self._authenticate()
        self.shopping_cart = ShoppingCart(self)

    def _authenticate(self):
        data = {'userName': self.username,
                'password': self.password,
                'rememberUser': True}
        url = '{base}/mijn/inloggen/basis'.format(base=self.url)
        response = self.session.post(url, data=data)
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
        success_url = '{base}{redirect}'.format(base=self.url,
                                                redirect=redirect)
        self.session.get(success_url)
        return True


class ShoppingCart(object):
    def __init__(self, ah_instance):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                               suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self._ah = ah_instance
        self._url = ('{base}/service/rest/shoppinglists/0/'
                     'items').format(base=self._ah.url)

    def add_item_by_id(self, item_id, quantity=1):
        return self._add_item('PRODUCT', 'id', item_id, quantity)

    def add_item_by_description(self, description, quantity=1):
        return self._add_item('UNSPECIFIED',
                              'description',
                              description,
                              quantity)

    def _add_item(self, submission_type, item_type, item_info, quantity):
        data = {'type': submission_type,
                'item': {item_type: item_info},
                'quantity': int(quantity)}
        response = self._ah.session.post(self._url, json=data)
        return response.ok

    @property
    def contents(self):
        url = ('{base}/service/rest/delegate'
               '?url=%2Fmijnlijst').format(base=self._ah.url)
        response = self._ah.session.get(url)
        data = response.json()
        items_lanes = [lane for lane in data['_embedded']['lanes']
                       if lane['type'] == 'ShoppingListLane']

        products = [ItemFactory(self._ah, item)
                    for cart in items_lanes
                    for item in cart.get('_embedded').get('items')]
        return products

    def get_items_with_discount(self):
        return [item for item in self.contents if item.has_discount]


class ItemFactory(object):
    def __new__(cls, ah_instance, info):
        print info
        product_type = info.get('type').lower()
        if product_type == 'product':
            return Product(ah_instance, info)
        elif product_type == 'unspecifieditem':
            return UnspecifiedProduct(ah_instance, info)


class Item(object):
    def __init__(self, ah_instance, info):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                               suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self._ah = ah_instance
        self._info = info

    @property
    def url(self):
        _url = self._info.get('navItem', {}).get('link', {}).get('href', {})
        return self._ah.url + _url


class UnspecifiedProduct(Item):
    def __init__(self, ah_instance, info):
        super(UnspecifiedProduct, self).__init__(ah_instance, info)

    @property
    def description(self):
        description = self._info.get('description')
        return description.replace(u'\xad', u'')

    def __getattr__(self, attribute):
        item = self.__dict__.get(attribute)
        if not item:
            message = ('Unspecified Products do not support all the '
                       'attributes of Products. {} is not a supported '
                       'attribute'.format(attribute))
            self._logger.warning(message)
        return item


class Product(Item):
    def __init__(self, ah_instance, info):
        super(Product, self).__init__(ah_instance, info)

    @property
    def _product(self):
        return self._info.get('_embedded').get('product')

    @property
    def id(self):
        return self._product.get('id')

    @property
    def is_orderable(self):
        return self._product.get('availability', {}
                                ).get('orderable', False)

    @property
    def category(self):
        return self._product.get('categoryName')

    @property
    def price(self):
        return self._product.get('priceLabel', {}).get('now')

    @property
    def price_previously(self):
        return self._product.get('priceLabel', {}).get('was')

    @property
    def has_discount(self):
        discount = self._product.get('discount')
        return True if discount else False

    @property
    def measurement_unit(self):
        return self._product.get('unitSize')

    @property
    def description(self):
        description = self._product.get('description')
        return description.replace(u'\xad', u'')

    @property
    def brand(self):
        return self._product.get('brandName')
