from abc import ABC, abstractmethod
from typing import List

from bookstore.models import User, Book


class BookSearchCategory:
    ID = 0
    TITLE = 1
    AUTHOR = 2
    CATEGORY = 3
    PUBLISHER = 4
    ISBN = 5
    DISCOUNT = 6


class AbstractDatabasesConnector(ABC):

    @abstractmethod
    def get_user(self, email: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def add_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> bool:
        pass

    @abstractmethod
    def search_books(self, category: BookSearchCategory, search_text: str, operator: str = None) -> List[Book]:
        pass
