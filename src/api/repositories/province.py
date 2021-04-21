from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import ProvinceModel, ProvinceSchema


class ProvinceRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = ProvinceModel
        self.schema = ProvinceSchema()
        self.schemas = ProvinceSchema(many=True)
        self._attr_id = 'id'
        self.default_sort_key = 'created_timestamp'
        self.allowed_sort_keys = ['name', 'is_pickup_available']
        self.allowed_filter_keys = ['name', 'is_pickup_available']
        self.creatable_fields = ['name', 'is_pickup_available']
        self.updatable_fields = ['name', 'is_pickup_available']
