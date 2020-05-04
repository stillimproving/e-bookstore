from flask import Flask

app = Flask(__name__)
logger = app.logger

from bookstore.bookstore_web import routes
