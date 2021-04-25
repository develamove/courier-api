from flask import Flask
from sqlalchemy.exc import OperationalError
from src.configs import DatabaseConfig, ServerConfig
from src.error_handlers import *
from src.extensions import cors, database, marshmallow, jwt, bcrypt


def create_app():
    """Construct the core application."""
    application = Flask(__name__)
    database_config = DatabaseConfig()
    mysql_uri = 'mysql+pymysql://' + database_config.__getattribute__('DB_MYSQL_USERNAME') + \
                ':' + database_config.__getattribute__('DB_MYSQL_PASSWORD') + \
                '@' + database_config.__getattribute__('DB_MYSQL_HOST') + \
                '/' + database_config.__getattribute__('DB_MYSQL_DATABASE')
    application.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_POOL_RECYCLE'] = 90
    application.config['JWT_SECRET_KEY'] = 'courier_secret_key'

    cors.init_app(application, resources={r'/*': {'origins': '*'}})
    database.init_app(application)
    marshmallow.init_app(application)
    jwt.init_app(application)
    bcrypt.init_app(application)

    with application.app_context():
        # Add error handlers
        application.register_error_handler(OperationalError, handle_db_error)

        # Initialize globals/extensions in app context
        # import routes here
        from src.api.controllers import staffs, clients, deliveries, locations

        application.register_blueprint(staffs)
        application.register_blueprint(clients)
        application.register_blueprint(deliveries)
        application.register_blueprint(locations)

    return application


app = create_app()
server_config = ServerConfig()
if __name__ == "__main__":
    app.run(
        host=server_config.APPS_HOST,
        port=server_config.APPS_PORT,
        debug=True
    )
