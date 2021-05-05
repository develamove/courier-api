from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.utils import response_creator, get_request_data, protected, SUCCESS

auth = Blueprint('Authentication', __name__, url_prefix='/auth')


@auth.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
@response_creator
def refresh_token(**kwargs):
    data = get_request_data(request, **kwargs)
    # identity = get_jwt_identity()
    # access_token = create_access_token(identity=identity)
    return dict(access_token=''), [], SUCCESS
