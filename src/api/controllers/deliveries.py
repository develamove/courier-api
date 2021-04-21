from flask import Blueprint, request
from src.api.services import DeliveryService
from src.utils import response_creator, get_request_data, protected

deliveries = Blueprint('Deliveries', __name__, url_prefix='/deliveries')
delivery_service = DeliveryService()


@deliveries.route('<filter_id>')
@response_creator
def get_delivery(filter_id: any, **kwargs):
    """Get a single delivery using a filter_id can be either (tracking_id or receipt_id (waybill)). To enable search
    using receipt_id assign a query parameter filter_key with a value receipt_id.

    Args:
        filter_id (any): ID that will be used for searching

    Returns:
        a single delivery resource, errors, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.get_delivery(filter_id, data)


@deliveries.route('<delivery_id>/info')
@response_creator
def get_delivery_info(delivery_id: int):
    """Get the sender and recipient information

    Args:
        delivery_id (int): unique ID of the delivery

    Returns:
        a single delivery resource, error, http status code
    """
    return delivery_service.get_delivery_info(delivery_id)


@deliveries.route('clients/<client_id>')
# @protected('all')
@response_creator
def get_client_deliveries(client_id: int, **kwargs):
    """Get a list of deliveries created by a specific client

    Args:
        client_id (int): unique ID of the client

    Returns:
        a multiple delivery resources, error, http status code
    """
    data = get_request_data(request, **kwargs)
    data['client_id'] = client_id

    return delivery_service.get_deliveries(data)


@deliveries.route('')
# @protected('admin')
@response_creator
def get_deliveries(**kwargs):
    """Get a list of all deliveries created

    Returns:
        a multiple delivery resources, error, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.get_deliveries(data)


@deliveries.route('<delivery_id>/logs')
# @protected('all')
@response_creator
def get_delivery_logs(delivery_id, **kwargs):
    """Get a list of deliveries created by a specific client

    Args:
        delivery_id (int): unique ID of the delivery

    Returns:
        a multiple delivery logs resources, error, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.get_delivery_logs(delivery_id, data)


@deliveries.route('', methods=['POST'])
# @protected('all')
@response_creator
def create_delivery(**kwargs):
    """Create a delivery

    Returns:
        a delivery status, error, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.create_delivery(data)


@deliveries.route('<delivery_id>', methods=['PUT'])
# @protected('all')
@response_creator
def modify_delivery(delivery_id, **kwargs):
    """Modify a delivery

    Args:
        delivery_id (int): unique ID of the delivery

    Returns:
        a delivery status, error, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.modify_delivery(delivery_id, data)
