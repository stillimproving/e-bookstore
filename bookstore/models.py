from flask_login import UserMixin


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


class User(UserMixin):
    def __init__(self, user_id: str = None, name: str = None, surname: str = None, password: str = None,
                 street: str = None, email: str = None, phone: str = None, postal_code: str = None, city: str = None,
                 country: str = None):
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


    def __str__(self):
        return str(self.name + ' ' + self.surname)

    def check_passwd(self, password):
        if self.password!=password:
            return False
        return True

    def get_id(self):
        return self.email


class Cart:
    _cart=dict()

    @classmethod
    def add_to_cart(cls, user_id, book_id, quantity):
        cart = cls._cart.get(user_id)
        if cart:
            cls._cart[user_id][book_id]=quantity
        else:
            my_cart={book_id: quantity}
            cls._cart[user_id]=my_cart
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
