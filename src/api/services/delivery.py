import datetime
from src.api.repositories import DeliveryRepository, DeliveryStatusRepository, SenderRepository, RecipientRepository, \
    EventRepository
from src.api.services.validation_schema import create_delivery_schema, fetch_delivery_schema, \
    fetch_delivery_status_schema, modify_delivery_schema, create_event_schema
from src.utils import create_tracking_id, filter_dict, format_cp_no, CustomValidator, ErrorManager, FAILURE, SUCCESS, \
    DELIVERY_CREATION_FAILED, DELIVERY_CREATION_SUCCESS, DELIVERY_UPDATE_FAILED, DELIVERY_UPDATE_SUCCESS


class DeliveryService:
    delivery_repo = DeliveryRepository()
    event_repo = EventRepository()
    status_repo = DeliveryStatusRepository()
    sender_repo = SenderRepository()
    recipient_repo = RecipientRepository()
    status_keys = ['is_for_pick_up', 'is_already_pick_up', 'is_in_transit', 'is_remitted', 'is_delivered',
                   'is_successful', 'is_cancelled']

    def get_delivery(self, filter_id: any, data: any):
        """Get a single delivery using a filter_id can be either (tracking_id or receipt_id (waybill))

        Args:
            filter_id (any): key for searching specific delivery
            data (any): an object which holds the information of the request

        Returns:
            a single delivery resource, errors, and a HTTP status code
        """
        filter_keys = ['tracking_id', 'receipt_id']
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
        for event in raw_events:
            raw = dict()
            raw['delivery_id'] = delivery_id
            raw['name'] = event.get('name')
            raw['remarks'] = event.get('remarks', '')
            validator = CustomValidator(create_event_schema, allow_unknown=True)
            validator.validate(raw)

            if validator.errors:
                return '', validator.errors, FAILURE

            events.append(raw)

        self.event_repo.bulk_add(events)
        return '', dict(), SUCCESS

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

    def create_delivery(self, data):
        """Get a list of deliveries

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

            data['tracking_id'] = create_tracking_id()
            # Transform the cellphone number
            data['sender']['cellphone_no'] = format_cp_no(data['sender']['cellphone_no'])
            data['recipient']['cellphone_no'] = format_cp_no(data['sender']['cellphone_no'])

            is_tracking_id_exist = self.delivery_repo.get_by_attributes_first(['tracking_id'], data)
            if is_tracking_id_exist:
                data['tracking_id'] = create_tracking_id()
            delivery_data = filter_dict(self.delivery_repo.field_keys, data)
            delivery = self.delivery_repo.add(delivery_data)
            if not delivery:
                return DELIVERY_CREATION_FAILED, validator.errors, FAILURE

            data['sender']['delivery_id'] = delivery.id
            sender = self.sender_repo.add(data['sender'])

            if not sender:
                return DELIVERY_CREATION_FAILED, validator.errors, FAILURE

            data['recipient']['delivery_id'] = delivery.id
            recipient = self.recipient_repo.add(data['recipient'])

            if not recipient:
                return DELIVERY_CREATION_FAILED, validator.errors, FAILURE

            return DELIVERY_CREATION_SUCCESS, '', SUCCESS

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

        # Keys for admin ['is_for_pick_up', 'is_already_pick_up', 'is_in_transit', 'is_delivered',
        # 'is_successful', 'is_remitted']

        if not validator.errors:
            # if data['identity_role'] == 'client' and str(data['client_id']) != str(data['identity_id']):
            #     return DELIVERY_CREATION_FAILED, dict(client=['invalid client id']), FAILURE
            # if data['identity_role'] == 'admin':
            #     data['client_id'] = 0

            is_delivery_exist = self.delivery_repo.get_by_attributes_first(['id'], cached_data)
            if not is_delivery_exist:
                errors = ErrorManager.create_error('delivery', 'delivery not exist')
                return DELIVERY_UPDATE_FAILED, errors, FAILURE

            filtered_data = filter_dict(self.delivery_repo.updatable_fields, data)
            if len(filtered_data) > 0:
                filtered_data['set_timestamp'] = datetime.datetime.now()
                delivery = self.delivery_repo.update(delivery_id, filtered_data)

                if not delivery:
                    errors = ErrorManager.create_error('delivery', 'update failed')
                    return DELIVERY_UPDATE_FAILED, errors, SUCCESS

                if self._is_status_key_exist(filtered_data):
                    message, errors, status = self.create_delivery_status(delivery_id, data)
                    if status == FAILURE:
                        return message, errors, status

            if 'sender' in data:
                data['sender']['set_timestamp'] = datetime.datetime.now()
                sender = self.sender_repo.get_by_attributes_first(['delivery_id'], {'delivery_id': delivery_id})
                if not sender:
                    errors = ErrorManager.create_error('delivery', 'sender not exist')
                    return DELIVERY_UPDATE_FAILED, errors, FAILURE
                sender_status = self.sender_repo.update(sender.id, data['sender'])

                if not sender_status:
                    return DELIVERY_UPDATE_FAILED, '', FAILURE

            if 'recipient' in data:
                data['recipient']['set_timestamp'] = datetime.datetime.now()
                recipient = self.recipient_repo.get_by_attributes_first(['delivery_id'], {'delivery_id': delivery_id})
                if not recipient:
                    errors = ErrorManager.create_error('delivery', 'recipient not exist')
                    return DELIVERY_UPDATE_FAILED, errors, SUCCESS
                recipient_status = self.recipient_repo.update(recipient.id, data['recipient'])

                if not recipient_status:
                    return DELIVERY_UPDATE_FAILED, '', FAILURE

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
