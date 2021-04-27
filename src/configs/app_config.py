from .base_config import BaseConfig


class AppConfig(BaseConfig):
    """This is the class for the environment configuration"""

    def __init__(self) -> None:
        """Constructor of the applications configuration
        """

        self.config_keys = ['JWT_SECRET']
        super().__init__()

        self.JWT_SECRET = str(self.JWT_SECRET)
        """Secret key for JWT tokens"""
