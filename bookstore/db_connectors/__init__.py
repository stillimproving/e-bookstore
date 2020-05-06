from .connector import DatabasesConnector
from .restdb_io import RestDBioConnector


db = DatabasesConnector(RestDBioConnector())
