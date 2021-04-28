import platform
import pdfkit
import os
import subprocess
from datetime import datetime
from flask import Blueprint, request, make_response, render_template
from src.api.services import DeliveryService
from src.utils import response_creator, get_request_data, protected

deliveries = Blueprint('Deliveries', __name__, url_prefix='/deliveries')
delivery_service = DeliveryService()

if platform.system() == 'Windows':
    pdfkit_config = pdfkit.configuration(
        wkhtmltopdf=os.environ.get('WKHTMLTOPDF_PATH', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    )
else:
    WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_PATH', '/app/bin/wkhtmltopdf')],
                                       stdout=subprocess.PIPE).communicate()[0].strip()
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

delivery_template = {
    "cancellation_reason": "cancellation reason",
    "client_id": 10000,
    "created_timestamp": "2021-04-28 11:53:38",
    "failure_reason": "failure reason",
    "id": 45,
    "insurance_fee": 0,
    "item_description": "This is a sample package name",
    "item_type": "M",
    "item_value": 100,
    "payment_method": "cod",
    "receipt_id": "123123",
    "recipient": {
        "cellphone_no": "+639096309187",
        "city": "Pasig City",
        "created_timestamp": "2021-04-28 11:53:38",
        "delivery_id": 45,
        "district": "Rosario",
        "email": "",
        "full_name": "Sender Full Name",
        "id": 43,
        "landmarks": "Near SM Ortigas",
        "postal_code": "0000",
        "province": "Metro Manila",
        "street": "Gumamela st",
        "updated_timestamp": 'null'
    },
    "remarks": "sample remarks",
    "sender": {
        "cellphone_no": "+639096309187",
        "city": "Pasig City",
        "created_timestamp": "2021-04-28 11:53:38",
        "delivery_id": 45,
        "district": "Rosario",
        "email": "",
        "full_name": "Sender Full Name",
        "id": 43,
        "landmarks": "Near SM Ortigas",
        "postal_code": "0000",
        "province": "Metro Manila",
        "street": "Gumamela st",
        "updated_timestamp": 'null'
    },
    "shipping_fee": 230,
    "status": "in_transit",
    "total": 230,
    "tracking_number": "HCAE-6776-4885",
    "updated_timestamp": "2021-04-28 23:09:08"
}


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


@deliveries.route('/<delivery_id>/events')
@response_creator
def get_delivery_events(delivery_id: any, **kwargs):
    """Get all events occurred on a specific delivery/transaction

    Args:
        delivery_id (any): a unique ID of the delivery/transaction

    Returns:
        a single delivery resource, errors, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.get_delivery_events(delivery_id, data)


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


@deliveries.route('<delivery_id>/events', methods=['POST'])
# @protected('all')
@response_creator
def create_delivery_events(delivery_id, **kwargs):
    """Create a delivery

    Returns:
        a delivery status, error, http status code
    """
    data = get_request_data(request, **kwargs)

    return delivery_service.create_delivery_events(delivery_id, data)


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


def convert_item_type(item_key: str):
    item_types = {
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large',
        'B': 'Box',
        'OWN': 'Own Packaging'
    }

    return item_types[item_key]


@deliveries.route('<delivery_id>/receipts')
def download_receipt(delivery_id, **kwargs):
    data = get_request_data(request, **kwargs)
    data['filter_key'] = 'id'
    delivery_info, _, _ = delivery_service.get_delivery(delivery_id, data)
    if len(delivery_info['delivery']) == 0:
        return dict(error={'errors': 'delivery not found'}), 200

    delivery_raw = delivery_template.copy()
    delivery_raw.update(delivery_info)

    # Convert the necessary data
    created_timestamp = datetime.strptime(delivery_raw['created_timestamp'], '%Y-%m-%d %H:%M:%S')
    delivery_raw['created_timestamp'] = created_timestamp.strftime('%B %m, %Y')
    item_type = convert_item_type(delivery_raw['item_type'])
    delivery_raw['item_type'] = item_type
    payment_method = 'Cash on Delivery' if delivery_raw['payment_method'] == 'cod' else 'non Cash on Delivery'
    delivery_raw['payment_method'] = payment_method

    html = render_template('receipt.html', json_data=delivery_raw)
    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)
    response = make_response(pdf)
    tracking_number = delivery_raw.get('tracking_number', 'receipt')
    content_disposition = 'attachment; filename=trasanction-' + tracking_number + '.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = content_disposition

    return response
