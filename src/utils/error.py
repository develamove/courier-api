
class Error:
    errors = []

    @staticmethod
    def create_error_inst():
        return Error()

    def add(self, error: object):
        self.errors.append(error)

    def get_all(self):
        return self.errors

    def has_error(self):
        return len(self.errors) > 0
