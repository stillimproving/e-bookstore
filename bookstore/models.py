class Book:
    def __init__(self, book_id: str, title: str = None, author: str = None, category: str = None, publisher: str = None,
                 isbn: str = None, release: str = None, language: str = None, pages: str = None, hardcover: str = None,
                 cover: str = None, quantity: int = None, price: int = None, discount: int = None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.publisher = publisher
        self.isbn = isbn
        self.release = release
        self.language = language
        self.pages = pages
        self.hardcover = hardcover
        self.cover = cover
        self.quantity = quantity
        self.price = price
        self.discount = discount


class User:
    def __init__(self, user_id: str, name: str = None, surname: str = None, password: str = None, street: str = None,
                 email: str = None, phone: str = None, postal_code: str = None, city: str = None, country: str = None):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.password = password
        self.street = street
        self.email = email
        self.phone = phone
        self.postal_code = postal_code
        self.city = city
        self.country = country
