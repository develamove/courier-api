from flask_jwt_extended import create_access_token
from src.api.services.validation_schema import fetch_client_schema, register_client_schema, modify_client_schema
from src.api.repositories import ClientRepository
from src.utils import filter_dict, CustomValidator, FAILURE, SUCCESS


class ClientService:
    client_repo = ClientRepository()

    def login_client(self, data: any):
        """Login using client details

        Args:
            data (any): an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        client_resource = self.client_repo.get_by_attributes_first(['username'], data, verify_password=True)
        if client_resource:
            username = data.get('username', '')
            client = self.client_repo.dump(client_resource)
            claims = {
                'identity_role': 'client',
                'identity_id': client['id']
            }
            access_token = create_access_token(identity=username, additional_claims=claims)
            return dict(token=access_token, client_id=client['id']), [], SUCCESS

        return dict(), dict(credentials=['not valid credentials']), FAILURE

    def get_clients(self, data: any):
        """Get a list of clients

        - sort_by:
        - sort_by: asc and desc
        - limit: 100 (default)
        - page: 1 (default)
        - returns a list of staffs
        Args:
            data: an object which holds the information of the request

        Returns:
            a resources, errors, and the status
        """
        validator = CustomValidator(fetch_client_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            clients = self.client_repo.get_by_attributes(data)
            resources = self.client_repo.dump(clients.items, True)
            return dict(clients=resources, total=clients.total), [], SUCCESS

        return dict(), validator.errors, FAILURE

    def register_client(self, data):
        """Register a new client

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        validator = CustomValidator(register_client_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            is_username_exist = self.client_repo.get_by_attributes_first(['username'], data)
            if is_username_exist:
                return [], dict(username=['already exist']), FAILURE

            is_email_exist = self.client_repo.get_by_attributes_first(['email'], data)
            if is_email_exist:
                return [], dict(email=['already exist']), FAILURE

            client = self.client_repo.add(data)
            if client:
                client_resource = self.client_repo.dump(client)
                return client_resource, dict(), SUCCESS
        return 'failed to create staff', validator.errors, FAILURE

    def modify_client(self, client_id, data):
        """Register a new client

        Args:
            client_id: id of the resource
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        validator = CustomValidator(modify_client_schema, allow_unknown=True)
        validator.validate(data)
        data['id'] = client_id

        if not validator.errors:
            is_client_exist = self.client_repo.get_by_attributes_first(['id'], data)
            if not is_client_exist:
                return 'client not exist', '', FAILURE

            filtered_data = filter_dict(self.client_repo.updatable_fields, data)
            client = self.client_repo.update(client_id, filtered_data)
            if client:
                return 'success to update new client', '', SUCCESS

        return 'failed to update client', validator.errors, FAILURE
