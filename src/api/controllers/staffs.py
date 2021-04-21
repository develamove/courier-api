from flask import Blueprint, request
from src.api.services.staff import StaffService
from src.utils import response_creator, get_request_data, protected

staffs = Blueprint('Staffs', __name__, url_prefix='/staffs')
staff_service = StaffService()


@staffs.route('')
@protected('admin')
@response_creator
def get_staffs(**kwargs):
    data = get_request_data(request, **kwargs)

    return staff_service.get_staffs(data)


@staffs.route('/login', methods=['POST'])
@response_creator
def login_staff():
    data = get_request_data(request)

    return staff_service.login_staff(data)


@staffs.route('', methods=['POST'])
# @protected('admin')
@response_creator
def register_staffs(**kwargs):
    data = get_request_data(request, **kwargs)

    return staff_service.register_staff(data)
