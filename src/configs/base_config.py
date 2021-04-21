from typing import List

from dotenv import load_dotenv
import os

from ..utils import MissingConfigKeyError


class BaseConfig:

    config_keys: List[str] = []

    def __init__(self):
        load_dotenv()
        self.app_env = os.getenv('APPS_ENV', 'dev')
        self.set_attributes()

    def set_attributes(self):
        for key in self.config_keys:
            value = os.getenv(key)
            if not value:
                raise MissingConfigKeyError(key)
            self.__setattr__(key, value)
