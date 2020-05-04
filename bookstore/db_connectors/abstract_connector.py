from abc import ABC, abstractmethod
from typing import List

from bookstore.models import User, Book


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
    def del_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def get_books(self, book_id: str = None, title: str = None, author: str = None, category: str = None,
                  publisher: str = None, isbn: str = None) -> List[Book]:
        pass

    @abstractmethod
    def update_book_quantity(self, book_id: str, quantity: int) -> bool:
        pass
