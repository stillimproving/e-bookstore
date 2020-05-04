from .connector import DatabasesConnector
from .restdb_io import RestDBioConnector


db_connector = DatabasesConnector(RestDBioConnector())
