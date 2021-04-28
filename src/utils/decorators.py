from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from src.utils import FAILURE, SERVER_ERROR


def response_creator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, errors, status_key = func(*args, **kwargs)

        status_code = 200
        if status_key == FAILURE:
            status_key = 422
        if status_key == SERVER_ERROR:
            status_code = 500

        response = {
            'status': status_code,
            'data': result,
            'msg': '',
            'errors': errors
        }

        return jsonify(response), status_code

    return wrapper


def admin_only():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] == 'admin':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


def protected(role: str = 'client'):
    """Endpoint guard using the jwt token

    Args:
        role (str): role of the client

    Returns:
        a HTTP status code
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            allowed_roles = ['client', 'admin', 'all']

            if role not in allowed_roles:
                return jsonify(msg='Forbidden'), 403

            if (claims['identity_role'] == 'admin' and role == 'admin') or (claims['identity_role'] == 'client'
                                                                            and role == 'client') or role == 'all':
                kwargs['identity_role'] = claims.get('identity_role', '')
                kwargs['identity_id'] = claims.get('identity_id', '')
                return fn(*args, **kwargs)
            else:
                return jsonify(msg='Forbidden, admins only!'), 403

        return decorator

    return wrapper
