from .base_config import BaseConfig


class DatabaseConfig(BaseConfig):
    """This is the class for the environment configuration"""

    def __init__(self) -> None:
        """Constructor of the database configuration
        """

        self.config_keys = ['DB_MYSQL_USERNAME', 'DB_MYSQL_PASSWORD', 'DB_MYSQL_HOST', 'DB_MYSQL_DATABASE']
        super().__init__()

        self.DB_MYSQL_USERNAME = str(self.DB_MYSQL_USERNAME)
        """Mysql username"""

        self.DB_MYSQL_PASSWORD = str(self.DB_MYSQL_PASSWORD)
        """Mysql password"""

        self.DB_MYSQL_HOST = str(self.DB_MYSQL_HOST)
        """Mysql host"""

        self.DB_MYSQL_DATABASE = str(self.DB_MYSQL_DATABASE)
        """Mysql database name"""
