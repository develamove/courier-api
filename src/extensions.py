# from flask import jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

cors = CORS()
database = SQLAlchemy()
marshmallow = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

# TODO change the jwt default error messages

# @jwt.expired_token_loader
# def my_expired_token_callback(jwt_header, jwt_payload):
#     return jsonify(code="dave", err="I can't let you do that"), 401
#
#
# @jwt.unauthorized_loader
# def my_expired_token_callback(jwt_header, jwt_payload):
#     return jsonify(code="dave", err="I can't let you do that"), 401
