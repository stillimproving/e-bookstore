from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
logger = app.logger
login = LoginManager(app)

from bookstore.bookstore_web import routes
