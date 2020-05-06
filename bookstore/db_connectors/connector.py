from typing import List

from .abstract_connector import AbstractDatabasesConnector, BookSearchCategory
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

    def update_book(self, book: Book) -> bool:
        return self._connector.update_book(book)

    def search_books(self, category: BookSearchCategory, search_text: str, operator: str = None) -> List[Book]:
        return self._connector.search_books(category, search_text, operator)
