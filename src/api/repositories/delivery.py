from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import DeliveryModel, DeliverySchema


class DeliveryRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = DeliveryModel
        self.schema = DeliverySchema()
        self.schemas = DeliverySchema(many=True)
        self._attr_id = 'id'
        self.field_keys = ['client_id', 'tracking_id', 'receipt_id', 'is_cod', 'is_provincial', 'is_for_pick_up',
                           'is_already_pick_up', 'is_remitted', 'is_delivered', 'is_successful', 'is_cancelled',
                           'item_name', 'item_type', 'item_amount', 'total_amount', 'comments', 'is_in_transit']
        self.creatable_fields = [
            'item_type', 'item_type', 'item_description', 'item_value', 'insurance_fee', 'shipping_fee', 'total',
            'payment_method', 'status', 'tracking_number', 'receipt_id', 'client_id', 'status'
        ]
        self.updatable_fields = ['receipt_id', 'is_cod', 'is_provincial', 'is_for_pick_up', 'is_already_pick_up',
                                 'is_in_transit', 'is_remitted', 'is_delivered', 'is_successful', 'is_cancelled',
                                 'item_name', 'item_type', 'item_amount', 'total_amount', 'comments', 'set_timestamp',
                                 'set_user', 'item_weight']
        self.allowed_sort_keys = []
        self.default_sort_key = 'created_timestamp'
        self.allowed_filter_keys = ['receipt_id', 'is_cod', 'is_provincial', 'is_for_pick_up', 'is_already_pick_up',
                                 'is_in_transit', 'is_remitted', 'is_delivered', 'is_successful', 'is_cancelled',
                                 'item_name', 'item_type', 'item_amount', 'total_amount', 'comments', 'set_timestamp',
                                 'set_user', 'item_weight', 'tracking_id', 'client_id']
