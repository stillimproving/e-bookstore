import yaml
from pathlib import Path

from bookstore.bookstore_web import logger
from bookstore.utils import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self.__config = dict()

    @property
    def _config(self):
        config_path = Path('config.yaml')
        try:
            with open(config_path, 'r') as config_file:
                self.__config = yaml.safe_load(config_file)
        except Exception as err:
            logger.error('Could not get config from file, err: ' + str(err))

        return self.__config

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._config.__getitem__(*args, **kwargs)

    def __str__(self):
        return str(self._config)
