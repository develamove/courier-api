from flask_jwt_extended import create_access_token
from src.api.models import StaffSchema
from src.api.services.validation_schema import fetch_staff_schema, register_staff_schema
from src.api.repositories import StaffRepository
from src.utils import CustomValidator, FAILURE, SUCCESS


class StaffService:
    staff_schema = StaffSchema()
    staff_repo = StaffRepository()
    staffs_schema = StaffSchema(many=True)

    def login_staff(self, data: any):
        username = data.get('username', '')
        staff_resource = self.staff_repo.get_by_attributes_first(['username'], data, verify_password=True)
        if staff_resource:
            staff = self.staff_repo.dump(staff_resource)
            claims = {
                'identity_role': 'admin',
                'identity_id': staff['id']
            }
            access_token = create_access_token(identity=username, additional_claims=claims)
            return dict(token=access_token), [], SUCCESS

        return dict(), 'please check the username or password', FAILURE

    def get_staffs(self, data: any):
        """Get a list of staffs

        - sort_by: username, role, and registered_timestamp
        - sort_by: asc and desc
        - limit: 100 (default)
        - page: 1 (default)
        - returns a list of staffs
        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        validator = CustomValidator(fetch_staff_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            staffs = self.staff_repo.get_by_attributes(data)
            staffs_list = [self.staff_schema.dump(staff) for staff in staffs.items]
            total = staffs.total
            return dict(staffs=staffs_list, total=total), [], SUCCESS
        return dict(), validator.errors, FAILURE

    def register_staff(self, data):
        """Register a staff

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        validator = CustomValidator(register_staff_schema, allow_unknown=True)
        validator.validate(data)

        if not validator.errors:
            is_username_exist = self.staff_repo.get_by_attributes_first(['username'], data)
            if is_username_exist:
                return 'user name already exist', '', FAILURE

            staff = self.staff_repo.add(data)
            if staff:
                return 'success to create new staff', '', SUCCESS

        return 'failed to create staff', validator.errors, FAILURE
