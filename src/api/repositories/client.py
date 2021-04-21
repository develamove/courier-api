from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import ClientModel, ClientSchema


class ClientRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = ClientModel
        self.schema = ClientSchema()
        self.schemas = ClientSchema(many=True)
        self._attr_id = 'id'
        self.allowed_sort_keys = ['first_name', 'middle_name', 'last_name', 'province', 'city', 'district', 'landmarks',
                                  'email', 'cellphone_no']
        self.default_sort_key = 'registered_timestamp'
        self.allowed_filter_keys = ['first_name', 'middle_name', 'last_name', 'province', 'city', 'district',
                                    'landmarks', 'email', 'cellphone_no']
        self.updatable_fields = ['first_name', 'middle_name', 'last_name', 'province', 'city', 'district', 'landmarks',
                                 'email', 'cellphone_no', 'set_timestamp']
