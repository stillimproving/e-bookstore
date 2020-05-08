import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


class DatabaseConfig(Config):
    HOST = 'https://bookstore-5217.restdb.io/rest/'
    APIKEY = '40bb4341d568dd36ea4383d40a2abd4d22d42'
