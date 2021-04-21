from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import DeliveryLogsModel, DeliveryLogSchema


class DeliveryStatusRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = DeliveryLogsModel
        self.schema = DeliveryLogSchema()
        self.schemas = DeliveryLogSchema(many=True)
        self._attr_id = 'id'
        self.field_keys = ['delivery_id', 'name', 'value', 'retry']
        self.allowed_sort_keys = []
        self.default_sort_key = 'created_timestamp'
        self.allowed_filter_keys = ['delivery_id', 'name', 'value', 'retry']
