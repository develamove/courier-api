import platform
import pdfkit
import os
import subprocess
from flask import Blueprint, request, send_from_directory, current_app, send_file, make_response, render_template
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

body = {
    "data": {
        "order_id": 123,
        "order_creation_date": "2020-01-01 14:14:52",
        "company_name": "Test Company",
        "city": "Test City",
        "state": "MH",
    }
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


@deliveries.route('<delivery_id>/receipts')
def download_receipt(delivery_id, **kwargs):
    html = render_template('receipt.html', json_data=body['data'])
    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)
    data = get_request_data(request, **kwargs)
    delivery_info = delivery_service.get_delivery(delivery_id, data)
    response = make_response(pdf)
    content_disposition = 'attachment; filename=receipt-' + delivery_id + '.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = content_disposition

    return response
