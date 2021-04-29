import datetime
from src.api.repositories import DeliveryRepository, DeliveryStatusRepository, SenderRepository, RecipientRepository, \
    EventRepository
from src.api.services.validation_schema import create_delivery_schema, fetch_delivery_schema, \
    fetch_delivery_status_schema, modify_delivery_schema, create_event_schema
from src.utils import create_tracking_id, filter_dict, format_cp_no, CustomValidator, ErrorManager
from src.utils.constants import *


class DeliveryService:
    delivery_repo = DeliveryRepository()
    event_repo = EventRepository()
    status_repo = DeliveryStatusRepository()
    sender_repo = SenderRepository()
    recipient_repo = RecipientRepository()
    status_keys = ['is_for_pick_up', 'is_already_pick_up', 'is_in_transit', 'is_remitted', 'is_delivered',
                   'is_successful', 'is_cancelled']

    FOR_PICKUP_STATUS = {
        'name': 'for_pickup',
        'delivery_id': 0,
        'remarks': 'For pickup'
    }



    EVENT_HIERARCHY = ['for_pickup', 'picked_up', 'in_transit', 'failed_delivery', 'delivered', 'cancelled']

    def get_delivery(self, filter_id: any, data: any):
        """Get a single delivery using a filter_id can be either (tracking_id or receipt_id (waybill))

        Args:
            filter_id (any): key for searching specific delivery
            data (any): an object which holds the information of the request

        Returns:
            a single delivery resource, errors, and a HTTP status code
        """
        filter_keys = ['tracking_id', 'receipt_id', 'id']
        filter_key = data.get('filter_key', 'tracking_id')
        if filter_key not in filter_keys:
            filter_key = 'tracking_id'

        filters = {filter_key: filter_id}
        resource = self.delivery_repo.get_by_attributes_first(filter_keys, filters)

        return dict(delivery=self.delivery_repo.dump(resource)), [], SUCCESS

    def get_delivery_info(self, delivery_id: int):
        """Get the sender and recipient information using the delivery_id

        Args:
            delivery_id (int): key for searching specific delivery

        Returns:
            a sender and recipient resource, errors, and a HTTP status code
        """
        filter_keys = ['delivery_id']
        data = {'delivery_id': delivery_id}
        sender_resource = self.sender_repo.get_by_attributes_first(filter_keys, data)
        recipient_resource = self.recipient_repo.get_by_attributes_first(filter_keys, data)
        info = {
            'sender': self.sender_repo.dump(sender_resource),
            'recipient': self.recipient_repo.dump(recipient_resource)
        }

        return info, [], SUCCESS

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
            deliveries = self.delivery_repo.get_by_attributes(data)
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

        return dict(logs=resources, total=events.total), [], SUCCESS

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

    def get_delivery_logs(self, delivery_id: int, data: any):
        """Get a list of deliveries

        - sort_by: username, role, and registered_timestamp
        - sort_by: asc and desc
        - limit: 100 (default)
        - page: 1 (default)
        - returns a list of deliveries

        Args:
            delivery_id (int):
            data: an object which holds the information of the request

        Returns:
            a resources, errors, and the status
        """

        validator = CustomValidator(fetch_delivery_status_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            data['delivery_id'] = delivery_id
            delivery_logs = self.status_repo.get_by_attributes(data)
            resources = self.status_repo.dump(delivery_logs.items, True)

            return dict(logs=resources, total=delivery_logs.total), [], SUCCESS

        return dict(), validator.errors, FAILURE

    @staticmethod
    def get_shipping_fee(sender_province_id, recipient_province_id, item_type):
        sender_code = 'lvm'
        recipient_code = 'lvm'

        if sender_province_id in MANILA_PROVINCE_ID:
            sender_code = 'm'
        elif sender_province_id in GREATER_MANILA_PROVINCE_ID:
            sender_code = 'gm'

        if recipient_province_id in MANILA_PROVINCE_ID:
            recipient_code = 'm'
        elif recipient_province_id in GREATER_MANILA_PROVINCE_ID:
            recipient_code = 'gm'

        location_fee_code = sender_code + '_to_' + recipient_code

        return SHIPPING_FEES[item_type.upper()][location_fee_code]

    def _get_delivery_computations(self, data):
        sender_province_id = data['sender'].get('province_id')
        recipient_province_id = data['recipient'].get('province_id')

        shipping_fee = DeliveryService.get_shipping_fee(sender_province_id, recipient_province_id, data.get('item_type'))
        if shipping_fee['fee'] == 0:
            return None

        return {
            'shipping_fee': shipping_fee['fee'],
            'total': shipping_fee['fee'],
            'insurance_fee': 0
        }

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
            # if data['identity_role'] == 'client' and str(data['client_id']) != str(data['identity_id']):
            #     return DELIVERY_CREATION_FAILED, dict(client=['invalid client id']), FAILURE
            # if data['identity_role'] == 'admin':
            #     data['client_id'] = 0

            # Static client id
            data['client_id'] = 10000
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
            # if data['identity_role'] == 'client' and str(data['client_id']) != str(data['identity_id']):
            #     return DELIVERY_CREATION_FAILED, dict(client=['invalid client id']), FAILURE
            # if data['identity_role'] == 'admin':
            #     data['client_id'] = 0

            data['client_id'] = 10000
            is_delivery_exist = self.delivery_repo.get_by_attributes_first(['id'], cached_data)
            if not is_delivery_exist:
                errors = ErrorManager.create_error('delivery', 'delivery not exist')
                return DELIVERY_UPDATE_FAILED, errors, FAILURE

            filtered_data = filter_dict(self.delivery_repo.updatable_fields, data)
            if len(filtered_data) > 0:
                if data.get('receipt_id', None) is not None:
                    is_receipt_id_exist = self.delivery_repo.get_by_attributes_first(['receipt_id'], data)
                    if is_receipt_id_exist:
                        return DELIVERY_CREATION_FAILED, dict(receipt_id=['receipt_id is already existing']), FAILURE

                filtered_data['updated_timestamp'] = datetime.datetime.now()
                delivery = self.delivery_repo.update(delivery_id, filtered_data)

                if not delivery:
                    errors = ErrorManager.create_error('delivery', 'failed to update the delivery')
                    return DELIVERY_UPDATE_FAILED, errors, SUCCESS

            # Disable to update the sender and recipient of the delivery
            # if 'sender' in data:
            #     data['sender']['set_timestamp'] = datetime.datetime.now()
            #     sender = self.sender_repo.get_by_attributes_first(['delivery_id'], {'delivery_id': delivery_id})
            #     if not sender:
            #         errors = ErrorManager.create_error('delivery', 'sender not exist')
            #         return DELIVERY_UPDATE_FAILED, errors, FAILURE
            #     sender_status = self.sender_repo.update(sender.id, data['sender'])
            #
            #     if not sender_status:
            #         return DELIVERY_UPDATE_FAILED, '', FAILURE
            #
            # if 'recipient' in data:
            #     data['recipient']['set_timestamp'] = datetime.datetime.now()
            #     recipient = self.recipient_repo.get_by_attributes_first(['delivery_id'], {'delivery_id': delivery_id})
            #     if not recipient:
            #         errors = ErrorManager.create_error('delivery', 'recipient not exist')
            #         return DELIVERY_UPDATE_FAILED, errors, SUCCESS
            #     recipient_status = self.recipient_repo.update(recipient.id, data['recipient'])
            #
            #     if not recipient_status:
            #         return DELIVERY_UPDATE_FAILED, '', FAILURE

            return DELIVERY_UPDATE_SUCCESS, '', SUCCESS
        return DELIVERY_UPDATE_FAILED, validator.errors, FAILURE

    def create_delivery_status(self, delivery_id, data):
        retry = data.get('retry', 1)
        if retry > 2:
            return DELIVERY_UPDATE_FAILED, dict(retry=['max of 2 attempts']), FAILURE

        logs = []
        for status_key in self.status_keys:
            log = {}
            if status_key in data:
                status = status_key.replace('is_', '')
                log['delivery_id'] = delivery_id
                log['retry'] = data['retry']
                log['name'] = status.upper()
                log['value'] = data[status_key]
                logs.append(log)
        self.status_repo.bulk_add(logs)
        return 'success', dict(), SUCCESS

    def _is_status_key_exist(self, data):
        for status_key in self.status_keys:
            if status_key in data:
                return True

        return False
