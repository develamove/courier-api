from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import StaffModel, StaffSchema


class StaffRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = StaffModel
        self.schema = StaffSchema()
        self.schemas = StaffSchema(many=True)
        self._attr_id = 'id'
        self.allowed_sort_keys = ['username', 'role']
        self.default_sort_key = 'registered_timestamp'
        self.allowed_filter_keys = ['username', 'role']
