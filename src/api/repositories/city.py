from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import CityModel, CitySchema


class CityRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = CityModel
        self.schema = CitySchema()
        self.schemas = CitySchema(many=True)
        self._attr_id = 'id'
        self.default_sort_key = 'created_timestamp'
        self.allowed_sort_keys = ['name', 'is_pickup_available']
        self.allowed_filter_keys = ['name', 'is_pickup_available', 'province_id']
        self.creatable_fields = ['name', 'is_pickup_available']
        self.updatable_fields = ['name', 'is_pickup_available']
