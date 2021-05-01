from src.api.repositories.mysql_repository import MySQLRepository
from src.api.models import DeliveryModel, DeliverySchema


class DeliveryRepository(MySQLRepository):

    def __init__(self):
        super().__init__()
        self._model = DeliveryModel
        self.schema = DeliverySchema()
        self.schemas = DeliverySchema(many=True)
        self._attr_id = 'id'
        self.creatable_fields = ['item_type', 'item_type', 'item_description', 'item_value', 'insurance_fee',
                                 'shipping_fee', 'total', 'payment_method', 'status', 'tracking_number', 'receipt_id',
                                 'client_id', 'status', 'transaction_total', 'service_fees_payor']
        self.updatable_fields = ['receipt_id', 'cancellation_reason', 'failure_reason', 'status', 'remarks',
                                 'updated_timestamp']
        self.allowed_sort_keys = []
        self.default_sort_key = 'created_timestamp'
        self.allowed_filter_keys = ['receipt_id', 'cancellation_reason', 'failure_reason', 'status', 'remarks',
                                    'updated_timestamp', 'client_id', 'tracking_number']
