import datetime
from src.api.repositories import DeliveryRepository, DeliveryStatusRepository, SenderRepository, RecipientRepository, \
    EventRepository
from src.api.services.validation_schema import create_delivery_schema, fetch_delivery_schema, modify_delivery_schema, \
    create_event_schema
from src.utils import create_tracking_id, filter_dict, format_cp_no, CustomValidator, ErrorManager
from src.utils.constants import *
from src.utils.provinces import PROVINCES


class DeliveryService:
    delivery_repo = DeliveryRepository()
    event_repo = EventRepository()
    status_repo = DeliveryStatusRepository()
    sender_repo = SenderRepository()
    recipient_repo = RecipientRepository()

    FOR_PICKUP_STATUS = {
        'name': 'for_pickup',
        'delivery_id': 0,
        'remarks': 'For pickup'
    }

    EVENT_HIERARCHY = ['for_pickup', 'picked_up', 'in_transit', 'failed', 'delivered', 'cancelled',
                       'remitted']

    def get_delivery(self, filter_id: any, data: any):
        """Get a single delivery using a filter_id can be either (tracking_id or receipt_id (waybill))

        Args:
            filter_id (any): key for searching specific delivery
            data (any): an object which holds the information of the request

        Returns:
            a single delivery resource, errors, and a HTTP status code
        """
        filter_keys = ['tracking_number', 'receipt_id', 'id']
        filter_key = data.get('filter_key')
        if filter_key not in filter_keys:
            filter_key = 'tracking_number'

        filters = {filter_key: filter_id}
        resource = self.delivery_repo.get_by_attributes_first(filter_keys, filters)

        return dict(delivery=self.delivery_repo.dump(resource)), [], SUCCESS

    def get_deliveries(self, data: any):
        """Get a list of deliveries

        - sort_by: username, role, and registered_timestamp
        - sort_by: asc and desc
        - limit: 100 (default)
        - page: 1 (default)
        - returns a list of deliveries

        Args:
            data: an object which holds the information of the request

        Returns:
            multiple delivery resources, errors, and a HTTP status code
        """
        validator = CustomValidator(fetch_delivery_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            if data['identity_role'] == 'client' and data['identity_id'] is None:
                return DELIVERY_CREATION_FAILED, dict(token=['invalid token']), FAILURE
            elif data['identity_role'] == 'client':
                data['client_id'] = data['identity_id']

            # Get the required fields
            allowed_fields = ['limit', 'page', 'client_id']
            filters = filter_dict(allowed_fields, data)
            deliveries = self.delivery_repo.get_by_attributes(filters)
            resources = self.delivery_repo.dump(deliveries.items, True)

            return dict(deliveries=resources, total=deliveries.total, page=data.get('page', 1)), [], SUCCESS

        return dict(), validator.errors, FAILURE

    def get_delivery_events(self, delivery_id: any, data: any):
        """Get the events occurred on a specific delivery

        Args:
            delivery_id (any): a unique ID for the delivery
            data (any): an object which holds the information of the request

        Returns:
            a multiple event resource, errors, and a HTTP status code
        """
        data['delivery_id'] = delivery_id
        events = self.event_repo.get_by_attributes(data)
        resources = self.status_repo.dump(events.items, True)

        return dict(events=resources, total=events.total), [], SUCCESS

    def create_delivery(self, data):
        """Get a list of deliveries

        Included validation:
            1. Do the initial input validation
                a. item_type: required, values(S, M, L, XL, B, OWN)
                b. item_description: required, max length of 50
                c. item_value: required, min value 0 and max value 1000000
                d. payment_method: required, values(cod, non-cod)
                e. receipt_id: optional, max length of 15
                f. sender:
                    i. full_name: required, max length of
                    ii. cellphone_no: required with proper format
                g. recipient:
                    i. full_name: required, max length of
                    ii. cellphone_no: required with proper format
            2. Check if the client_id is match on the given access_token else check if its admin token

        Flow
            1. Check the role of the client and get the client_id
            2. Create tracking number, check  if the generated tracking_number exist on the database if exist, create
            generate new one and use it.
            4. Check if the receipt_id is existing
            3. Do the computation
            4. Add the delivery information
            5. Add the sender information
            6. Add the recipient information
            8. Create event

        TODO
          - check the location using id's

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """

        validator = CustomValidator(create_delivery_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            if data['identity_role'] == 'client' and data['identity_id'] is None:
                return DELIVERY_CREATION_FAILED, dict(token=['invalid token']), FAILURE
            elif data['identity_role'] == 'client':
                data['client_id'] = data['identity_id']

            if data['identity_role'] == 'admin':
                data['client_id'] = 0

            # Static client id
            data['tracking_number'] = create_tracking_id()

            if data.get('receipt_id', None) is not None:
                is_receipt_id_exist = self.delivery_repo.get_by_attributes_first(['receipt_id'], data)
                if is_receipt_id_exist:
                    return DELIVERY_CREATION_FAILED, dict(receipt_id=['receipt_id is already existing']), FAILURE

            is_tracking_id_exist = self.delivery_repo.get_by_attributes_first(['tracking_id'], data)
            if is_tracking_id_exist:
                data['tracking_number'] = create_tracking_id()

            computations = self._get_delivery_computations(data)
            data.update(computations)
            delivery_info = filter_dict(self.delivery_repo.creatable_fields, data)
            delivery_info['status'] = 'for_pickup'
            delivery = self.delivery_repo.add(delivery_info)
            if not delivery:
                self.delivery_repo.do_rollback()
                return DELIVERY_CREATION_FAILED, dict(sender=['failed to create delivery']), FAILURE

            # Add sender information
            data['sender']['delivery_id'] = delivery.id
            data['sender']['cellphone_no'] = format_cp_no(data['sender']['cellphone_no'])
            sender_info = filter_dict(self.sender_repo.creatable_fields, data['sender'])
            sender = self.sender_repo.add(sender_info)
            if not sender:
                return DELIVERY_CREATION_FAILED, dict(sender=['failed to insert sender information']), FAILURE

            # Add recipient information
            data['recipient']['delivery_id'] = delivery.id
            data['recipient']['cellphone_no'] = format_cp_no(data['recipient']['cellphone_no'])
            recipient_info = filter_dict(self.recipient_repo.creatable_fields, data['recipient'])
            recipient = self.recipient_repo.add(recipient_info)
            if not recipient:
                return DELIVERY_CREATION_FAILED, dict(recipient=['failed to insert recipient information']), FAILURE

            event_info = self.FOR_PICKUP_STATUS.copy()
            event_info.update({'delivery_id': delivery.id})
            event = self.event_repo.add(event_info)
            if not event:
                return DELIVERY_CREATION_FAILED, dict(event=['failed to add delivery event information']), FAILURE

            # Return the resource
            created_delivery = self.delivery_repo.dump(data=delivery)
            return dict(delivery=created_delivery), dict(), SUCCESS

        return DELIVERY_CREATION_FAILED, validator.errors, FAILURE

    def create_delivery_events(self, delivery_id: any, data: any):
        """Create an events for a specific delivery

        Args:
            delivery_id (any): a unique ID for the delivery
            data (any): an object which holds the information of the request

        Returns:
            a multiple event resource, errors, and a HTTP status code
        """
        delivery = self.delivery_repo.get_by_id(delivery_id)
        resource = self.delivery_repo.dump(delivery)

        if resource == {}:
            return '', dict(delivery_id=['delivery not found']), SUCCESS

        raw_events = data.get('events', [])
        events = []
        status_name = 'for_pickup'
        status_index = 0
        for event in raw_events:
            raw = dict()
            name = event.get('name')
            raw['delivery_id'] = delivery_id
            raw['name'] = name
            raw['remarks'] = event.get('remarks', '')
            validator = CustomValidator(create_event_schema, allow_unknown=True)
            validator.validate(raw)

            if validator.errors:
                return '', validator.errors, FAILURE
            if status_index < self.EVENT_HIERARCHY.index(name):
                status_name = name
                status_index = self.EVENT_HIERARCHY.index(name)
            events.append(raw)
        event_resource = self.event_repo.bulk_add(events)
        if not event_resource:
            return '', dict(events=['can\'t add event to the given delivery']), SUCCESS

        delivery_resource = self.delivery_repo.update(delivery_id, {'status': status_name})
        if not delivery_resource:
            return '', dict(events=['failed to update the delivery']), SUCCESS
        return 'success to update the delivery', dict(), SUCCESS

    def modify_delivery(self, delivery_id, data):
        """Modify a delivery details

        Args:
            delivery_id: id of the resource
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        validator = CustomValidator(modify_delivery_schema, allow_unknown=True)
        validator.validate(data)
        cached_data = data
        cached_data['id'] = delivery_id

        if not validator.errors:
            if data['identity_role'] == 'client' and data['identity_id'] is None:
                return DELIVERY_CREATION_FAILED, dict(token=['invalid token']), FAILURE
            elif data['identity_role'] == 'client':
                data['client_id'] = data['identity_id']

            if data['identity_role'] == 'admin':
                data['client_id'] = 0

            is_delivery_exist = self.delivery_repo.get_by_attributes_first(['id'], cached_data)
            if not is_delivery_exist:
                errors = ErrorManager.create_error('delivery', 'delivery not exist')
                return DELIVERY_UPDATE_FAILED, errors, FAILURE

            # Check if the delivery is going to cancel
            is_for_cancellation = data.get('for_cancellation', 'F')
            if is_for_cancellation == 'T':
                data['status'] = 'cancelled'

            filtered_data = filter_dict(self.delivery_repo.updatable_fields, data)
            if len(filtered_data) > 0:
                if data.get('receipt_id', None) is not None:
                    is_receipt_id_exist = self.delivery_repo.get_by_attributes_first(['receipt_id'], data)
                    if is_receipt_id_exist:
                        return DELIVERY_CREATION_FAILED, dict(receipt_id=['receipt ID is already existing']), FAILURE

                filtered_data['updated_timestamp'] = datetime.datetime.now()
                delivery = self.delivery_repo.update(delivery_id, filtered_data)

                if not delivery:
                    errors = ErrorManager.create_error('delivery', 'failed to update the delivery')
                    return DELIVERY_UPDATE_FAILED, errors, SUCCESS

                if is_for_cancellation == 'T':
                    self.event_repo.add({
                        'delivery_id': data.get('id'),
                        'name': 'cancelled',
                        'remarks': data.get('cancellation_reason', '')
                    })

            return DELIVERY_UPDATE_SUCCESS, '', SUCCESS
        return DELIVERY_UPDATE_FAILED, validator.errors, FAILURE

    def _get_province(self, province_id):
        for province in PROVINCES:
            if province['id'] == province_id:
                return province

        return {
            "area": "metro_manila",
            "created_timestamp": "2021-04-21T04:59:45",
            "id": 49,
            "is_pickup_available": "T",
            "name": "Metro Manila"
          }

    def _get_delivery_computations(self, data):
        recipient_province_id = data['recipient'].get('province_id')
        selected_province = self._get_province(recipient_province_id)
        area = selected_province['area']
        item_type = data.get('item_type')
        item_value = data.get('item_value', 0)
        shipping_fee = SHIPPING_FEES[item_type][area]
        payor = data.get('service_fees_payor', 'sender')

        total = item_value
        if payor != 'sender':
            total = shipping_fee['fee'] + item_value

        return {
            'shipping_fee': shipping_fee['fee'],
            'transaction_total': shipping_fee['fee'],
            'insurance_fee': 0,
            'total': total
        }
