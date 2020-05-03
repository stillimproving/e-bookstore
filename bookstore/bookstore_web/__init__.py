from flask import Flask

app = Flask(__name__)

from bookstore.bookstore_web import routes
