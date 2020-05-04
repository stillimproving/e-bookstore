import requests
from typing import List
from json import dumps, loads

from bookstore.models import User, Book
from bookstore.config_service import Config
from bookstore.bookstore_web import logger

from .abstract_connector import AbstractDatabasesConnector


class RestDBioConnector(AbstractDatabasesConnector):
    _map_book = {
        'book_id': '_id',
        'title': 'Title',
        'author': 'Author',
        'category': 'Type',
        'publisher': 'Publisher',
        'isbn': 'ISBN',
        'release': 'Release',
        'language': 'Language',
        'pages': 'Pages',
        'hardcover': 'Hardcover',
        'cover': 'Cover',
        'quantity': 'Quantity',
        'price': 'Price',
        'discount': 'Discount'
    }
    _inv_map_book = {v: k for k, v in _map_book.items()}


    def __init__(self, config=None):
        self._config = config or Config()
        self._db_config = self._config.get('databases', {}).get('restdb.io', {})
        self.url = self._db_config.get('host')
        self.headers = {
            'content-type': "application/json",
            'x-apikey': self._db_config.get('apikey'),
            'cache-control': "no-cache"
        }

    def _add(self, values):
        try:
            response = requests.request("POST", self.url, data=dumps(values), headers=self.headers)
            return '_id' in response.text
        except requests.exceptions.ConnectionError:
            return False

    def _search(self, parameters):
        query = f'?q={dumps(parameters)}'
        try:
            response = requests.request("GET", self.url + query, headers=self.headers)
            return loads(response.text)
        except requests.exceptions.ConnectionError:
            return None

    def _delete(self, id):
        try:
            response = requests.request("DELETE", self.url + '/' + id, headers=self.headers)
            return id in response.text
        except requests.exceptions.ConnectionError:
            return False

    def _update(self, id, values):
        try:
            response = requests.request("PATCH", self.url + '/' + id, data=dumps(values), headers=self.headers)
            return id in response.text
        except requests.exceptions.ConnectionError:
            return False

    def get_user(self, email: str) -> User:
        pass

    def update_user(self, user: User) -> bool:
        pass

    def add_user(self, user: User) -> bool:
        pass

    def del_user(self, user: User) -> bool:
        pass

    def get_books(self, book_id: str = None, title: str = None, author: str = None, category: str = None,
                  publisher: str = None, isbn: str = None) -> List[Book]:

        parameters = {self._map_book[key]: val for key, val in locals().items()
                      if key in self._map_book and val is not None}
        query = f'?q={dumps(parameters)}'
        url = self.url + 'books' + query
        try:
            response = requests.request("GET", url, headers=self.headers)
            books = [{self._inv_map_book.get(key): val for key, val in book.items() if key in self._inv_map_book.keys()}
                     for book in loads(response.text)]
            return [Book(**book) for book in books]
        except requests.exceptions.ConnectionError as err:
            logger.error('Restdb.io connection error: ' + str(err))
            return []

    def update_book_quantity(self, book_id: str, quantity: int) -> bool:
        pass
