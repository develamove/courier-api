from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import EventModel, EventSchema


class EventRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = EventModel
        self.schema = EventSchema()
        self.schemas = EventSchema(many=True)
        self._attr_id = 'id'
        self.default_sort_key = 'created_timestamp'
        self.allowed_sort_keys = ['name', 'created_timestamp', 'updated_timestamp']
        self.allowed_filter_keys = ['name', 'delivery_id']
        self.creatable_fields = ['delivery_id', 'name', 'remarks']
        self.updatable_fields = ['name', 'remarks', 'updated_timestamp']
