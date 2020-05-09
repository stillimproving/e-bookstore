import requests
from json import dumps, loads

from config import DatabaseConfig


class RestDBioConnector:
    _url = DatabaseConfig.HOST
    _headers = {
        'content-type': "application/json",
        'x-apikey': DatabaseConfig.API_KEY,
        'cache-control': "no-cache"
    }

    @classmethod
    def add(cls, table, values):
        try:
            response = requests.request("POST", cls._url + table, data=dumps(values), headers=cls._headers)
        except requests.exceptions.ConnectionError:
            return None

        if '_id' in response.text:
            return loads(response.text)

        return None

    @classmethod
    def search(cls, table, params):
        query = f'?q={dumps(params)}'
        try:
            response = requests.request("GET", cls._url + table + query, headers=cls._headers)
            return loads(response.text)
        except requests.exceptions.ConnectionError:
            return []

    @classmethod
    def get(cls, table, key):
        try:
            response = requests.request("GET", cls._url + table + '/' + key, headers=cls._headers)
            return loads(response.text)
        except requests.exceptions.ConnectionError:
            return None

    @classmethod
    def delete(cls, table, key):
        try:
            response = requests.request("DELETE", cls._url + table + '/' + key, headers=cls._headers)
            return key in response.text
        except requests.exceptions.ConnectionError:
            return False

    @classmethod
    def update(cls, table, key, values):
        try:
            response = requests.request("PATCH", cls._url + table + '/' + key, data=dumps(values), headers=cls._headers)
            return key in response.text
        except requests.exceptions.ConnectionError:
            return False
