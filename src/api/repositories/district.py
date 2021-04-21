from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import DistrictModel, DistrictSchema


class DistrictRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = DistrictModel
        self.schema = DistrictSchema()
        self.schemas = DistrictSchema(many=True)
        self._attr_id = 'id'
        self.default_sort_key = 'created_timestamp'
        self.allowed_sort_keys = ['name', 'is_pickup_available']
        self.allowed_filter_keys = ['name', 'city_id', 'is_pickup_available']
        self.creatable_fields = ['name', 'is_pickup_available']
        self.updatable_fields = ['name', 'is_pickup_available']
