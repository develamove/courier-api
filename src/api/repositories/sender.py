from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import SenderModel, SenderSchema


class SenderRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = SenderModel
        self.schema = SenderSchema()
        self.schema_to_many = SenderSchema(many=True)
        self._attr_id = 'id'
        self.field_keys = ['full_name', 'cellphone_no', 'email', 'province', 'city', 'district', 'street', 'landmarks',
                           'set_timestamp', 'postal_code']
        self.updatable_fields = ['full_name', 'cellphone_no', 'email', 'province', 'city', 'district', 'street',
                                 'landmarks', 'set_timestamp', 'postal_code']
        self.allowed_sort_keys = []
        self.default_sort_key = 'created_timestamp'
        self.allowed_filter_keys = []
