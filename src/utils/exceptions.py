class MissingConfigKeyError(Exception):
    """Exception raised for missing config key"""

    def __init__(self, key="", message="Missing key '%s' in Config"):
        self.message = message % key
        super().__init__(self.message)
