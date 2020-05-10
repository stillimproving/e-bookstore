from datetime import datetime
from enum import Enum, unique

from flask_login import UserMixin

from bookstore.db_connector import RestDBioConnector as db
from bookstore.bookstore_web import login


@login.user_loader
def load_user(email):
    return CustomersDB.get(email)


@unique
class BookSearchCategory(Enum):
    ISBN = 'ISBN'
    TITLE = 'Title'
    AUTHOR = 'Author'
    CATEGORY = 'Type'
    PUBLISHER = 'Publisher'
    DISCOUNT = 'Discount'

    def __str__(self):
        return self.name


class Book:
    def __init__(self, book_id, title=None, author=None, category=None, publisher=None, isbn=None, release=None,
                 language=None, pages=None, hardcover=None, cover=None, quantity=None, price=None, discount=None,
                 cover_image=None):
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
        self.cover_image = cover_image

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return str(self.title)

    def __bool__(self):
        return bool(self.book_id)


class BooksDB:
    _tbl = 'books'
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
    _map_operators = {
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '<=': '$lte',
        'regex': '$regex'
    }

    @classmethod
    def get(cls, key):
        return cls._format_book(db.get(table=cls._tbl, key=key))

    @classmethod
    def get_by_isbn(cls, isbn: str):

        result = db.search(table=cls._tbl, params={'ISBN': isbn})
        if not result:
            return
        return result[0]

    @classmethod
    def search(cls, category: BookSearchCategory, search_text, operator: str = None):

        operator = operator or 'regex'

        query = {
            category.value: search_text if operator == '=' else {
                cls._map_operators.get(operator, '$regex'): search_text
            }
        }

        raw_books = db.search(table=cls._tbl, params=query)

        return [cls._format_book(raw_book) for raw_book in raw_books]

    @classmethod
    def reduce(cls, book: Book, count):
        if not book:
            return False
        values = {'$inc': {"Quantity": -count}}
        return db.update(table=cls._tbl, key=book.book_id, values=values)

    @classmethod
    def _format_book(cls, raw_books):
        book = {cls._inv_map_book.get(key): val for key, val in raw_books.items() if key in cls._inv_map_book.keys()}
        return Book(**book)


class Customer(UserMixin):
    def __init__(self, customer_id: str = None, name: str = None, surname: str = None, password: str = None,
                 street: str = None, email: str = None, phone: str = None, postal_code: str = None, city: str = None,
                 country: str = None):
        self.customer_id = customer_id
        self.name = name
        self.surname = surname
        self.password = password
        self.street = street
        self.email = email
        self.phone = phone
        self.postal_code = postal_code
        self.city = city
        self.country = country

    def __str__(self):
        return str(self.name + ' ' + self.surname)

    def __bool__(self):
        return bool(self.customer_id and self.email)

    def check_pass(self, password):
        if self.password != password:
            return False
        return True

    def get_id(self):
        return self.email


class CustomersDB:
    _tbl = 'customers'
    _map_user = {
        'customer_id': '_id',
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

    @classmethod
    def get(cls, email):
        raw_customer = db.search(table=cls._tbl, params={'Email': email})
        if raw_customer:
            return cls._format_customer(raw_customer[0])

    @classmethod
    def add(cls, customer: Customer):
        values = {cls._map_user[key]: val for key, val in vars(customer).items() if key in cls._map_user.keys()}
        return db.add(table=cls._tbl, values=values)

    @classmethod
    def delete(cls, customer: Customer):
        return db.delete(table=cls._tbl, key=customer.customer_id)

    @classmethod
    def update(cls, customer: Customer):
        values = {cls._map_user[key]: val for key, val in vars(customer).items() if key in cls._map_user.keys()}
        if customer.customer_id:
            return db.update(table=cls._tbl, key=customer.customer_id, values=values)
        return db.add(table=cls._tbl, values=values)

    @classmethod
    def _format_customer(cls, raw_customer):
        customer = {
            cls._inv_map_user.get(key): val for key, val in raw_customer.items() if key in cls._inv_map_user.keys()
        }
        return Customer(**customer)


class OrderDB:
    _tbl = 'orders'

    @classmethod
    def submit_order(cls, customer: Customer, total_price):
        customer_id = customer.customer_id
        customer_cart = Cart.pop_user_cart(customer_id)
        value = {
            'customer_id': customer_id,
            "status": "NEW",
            "date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'total_price': total_price,
            'cart': [{'book_id': book_id, 'quantity': quantity} for book_id, quantity in customer_cart.items()]
        }
        response = db.add(table=cls._tbl, values=value)
        order_id = response and response.get('order_id')
        if order_id:
            return order_id


class Cart:
    _cart = dict()

    @classmethod
    def add_to_cart(cls, user_id, book_id, quantity):
        cart = cls._cart.get(user_id)
        if cart:
            cls._cart[user_id][book_id] = quantity
        else:
            my_cart = {book_id: quantity}
            cls._cart[user_id] = my_cart
        return True

    @classmethod
    def remove_from_cart(cls, user_id, book_id):
        if cls._cart.get(user_id):
            cls._cart[user_id].pop(book_id, None)
            return True
        return False

    @classmethod
    def get_user_cart(cls, user_id):
        return cls._cart.get(user_id)

    @classmethod
    def pop_user_cart(cls, user_id):
        return cls._cart.pop(user_id, None)
