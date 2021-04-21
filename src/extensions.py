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
