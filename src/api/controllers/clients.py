from flask import Blueprint, request
from src.api.services import ClientService
from src.utils import response_creator, get_request_data, protected

clients = Blueprint('Clients', __name__, url_prefix='/clients')
client_service = ClientService()


@clients.route('')
@protected('admin')
@response_creator
def get_clients(**kwargs):
    data = get_request_data(request, **kwargs)
    return client_service.get_clients(data)


@clients.route('login', methods=['POST'])
@response_creator
def login_client(**kwargs):
    data = get_request_data(request, **kwargs)
    return client_service.login_client(data)


@clients.route('', methods=['POST'])
@response_creator
def register_client(**kwargs):
    data = get_request_data(request, **kwargs)

    return client_service.register_client(data)


@clients.route('<client_id>', methods=['PUT'])
@protected('all')
@response_creator
def modify_client(client_id):
    data = get_request_data(request)

    return client_service.modify_client(client_id, data)
