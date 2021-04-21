from .base_config import BaseConfig


class ServerConfig(BaseConfig):
    """This is the class for the environment configuration"""

    def __init__(self) -> None:
        """Constructor of the server configuration
        """

        self.config_keys = ['APPS_HOST', 'APPS_PORT']
        super().__init__()

        self.APPS_HOST = str(self.APPS_HOST)
        """Host where the server will be served"""

        self.APPS_PORT = int(self.APPS_PORT)
        """Port where the server will be served"""
