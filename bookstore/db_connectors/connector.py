from typing import List

from .abstract_connector import AbstractDatabasesConnector
from bookstore.utils import Singleton
from bookstore.models import User, Book


class DatabasesConnector(AbstractDatabasesConnector):
    __metaclass__ = Singleton

    def __init__(self, connector: AbstractDatabasesConnector):
        self._connector = connector

    def get_user(self, email: str) -> User:
        return self._connector.get_user(email)

    def update_user(self, user: User) -> bool:
        return self._connector.update_user(user)

    def add_user(self, user: User) -> bool:
        return self._connector.add_user(user)

    def delete_user(self, user: User) -> bool:
        return self._connector.delete_user(user)

    def get_books(self, book_id: str = None, title: str = None, author: str = None, category: str = None,
                  publisher: str = None, isbn: str = None) -> List[Book]:
        return self._connector.get_books(book_id, title, author, category, publisher, isbn)

    def update_book(self, book: Book) -> bool:
        return self._connector.update_book(book)
