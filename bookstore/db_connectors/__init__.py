from .connector import DatabasesConnector
from .restdb_io import RestDBioConnector
from bookstore.bookstore_web import login


db = DatabasesConnector(RestDBioConnector())

@login.user_loader
def load_user(email):
    return db.get_user(email)

