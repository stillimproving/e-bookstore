import requests
from typing import List, Union
from json import dumps, loads

from bookstore.models import User, Book
from bookstore.config_service import Config
from bookstore.bookstore_web import logger

from .abstract_connector import AbstractDatabasesConnector, BookSearchCategory


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
        'discount': 'Discount',
        'cover_image': 'Cover image',
    }
    _inv_map_book = {v: k for k, v in _map_book.items()}

    _map_user = {
        'user_id': '_id',
        'name': 'Name',
        'surname': 'Surname',
        'password': 'Password',
        'street': 'Street',
        'email': 'Email',
        'phone': 'Phone',
        'postal_code': 'Postal code',
        'city': 'City',
        'country': 'Country',
    }
    _inv_map_user = {v: k for k, v in _map_user.items()}

    _query_book_map = {
        BookSearchCategory.ISBN: 'ISBN',
        BookSearchCategory.ID: '_id',
        BookSearchCategory.TITLE: 'Title',
        BookSearchCategory.AUTHOR: 'Author',
        BookSearchCategory.CATEGORY: 'Type',
        BookSearchCategory.PUBLISHER: 'Publisher',
        BookSearchCategory.DISCOUNT: 'Discount',
    }

    def __init__(self, config=None):
        self._config = config or Config()
        self._db_config = self._config.get('databases', {}).get('restdb.io', {})
        self.url = self._db_config.get('host')
        self.headers = {
            'content-type': "application/json",
            'x-apikey': self._db_config.get('apikey'),
            'cache-control': "no-cache"
        }

    def _send_request(self, method, db, query=None, data=None, item_id=None):
        query = f'?q={dumps(query)}' if query else ''
        url = self.url + db + ('/' + item_id + query if item_id else query)
        try:
            response = requests.request(method, url, data=data, headers=self.headers)
        except requests.exceptions.ConnectionError as err:
            logger.error('Restdb.io connection error: ' + str(err))
            return []
        return response

    def delete_user(self, user: User) -> bool:
        response = self._send_request(method='DELETE', db='customers', item_id=user.user_id)
        return user.user_id in response.text

    def update_user(self, user: User) -> bool:
        data = {self._map_user[key]: val for key, val in vars(user).items() if key in self._map_user.keys()}
        response = self._send_request(method='PUT', db='customers', data=dumps(data), item_id=user.user_id)
        return user.user_id in response.text

    def add_user(self, user: User) -> bool:
        data = {self._map_user[key]: val for key, val in vars(user).items() if key in self._map_user.keys()}
        data.pop('_id')
        response = self._send_request(method='POST', db='customers', data=dumps(data))
        return '_id' in response.text

    def get_user(self, email: str) -> Union[User, None]:
        response = self._send_request(method='GET', db='customers', query={'Email': email})
        data = loads(response.text)
        if not data:
            return

        user_data = {self._inv_map_user.get(key): val for key, val in data[0].items()
                     if key in self._inv_map_user.keys()}

        return User(**user_data)

    def update_book(self, book: Book) -> bool:
        data = {self._map_user[key]: val for key, val in vars(book).items() if key in self._map_user.keys()}
        response = self._send_request(method='PUT', db='books', data=dumps(data), item_id=book.book_id)
        return book.book_id in response.text

    def search_books(self, category: BookSearchCategory, search_text: str, operator=None) -> List[Book]:

        query = {self._query_book_map[category]: self._query_method(category, search_text, operator)}

        response = self._send_request(method='GET', db='books', query=query)
        books = [{self._inv_map_book.get(key): val for key, val in book.items() if key in self._inv_map_book.keys()}
                 for book in loads(response.text)]
        return [Book(**book) for book in books]

    def _query_method(self, category: BookSearchCategory, search_text: str, operator=None):
        if category in [BookSearchCategory.ISBN, BookSearchCategory.ID] or operator == '=':
            return search_text
        if category == BookSearchCategory.DISCOUNT:
            operator = self._map_operators.get(operator) or '$gt'
            return {operator: search_text}
        return {"$regex": search_text}

    _map_operators = {
        '>': '$gt',
        '=>': '$gte',
        '<': '$lt',
        '=<': '$lte'
    }