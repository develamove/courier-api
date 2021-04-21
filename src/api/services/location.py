from cerberus import Validator
from src.api.services.base import BaseService
from src.api.repositories import ProvinceRepository, CityRepository, DistrictRepository
from src.utils import ERROR, SUCCESS


class LocationService(BaseService):
    province_repo = ProvinceRepository()
    city_repo = CityRepository()
    district_repo = DistrictRepository()

    def get_province(self, province_id):
        """Get a specific province using the its ID

        Args:
            province_id: an id for the resource

        Returns:
            a resource, errors, and the status
        """
        province = self.province_repo.get_by_id(province_id)

        return dict(province=self.province_repo.schema.dump(province)), [], SUCCESS

    def get_provinces(self, data):
        """Get a list of city, can be filtered using the allowed filters

        Args:
            data: an object which holds the information of the request

        Returns:
            a resources, errors, and the status
        """
        validator = Validator(self.get_validation_schema, allow_unknown=True)
        validator.validate(data, self.get_validation_schema)

        if validator.errors:
            return [], validator.errors, ERROR

        provinces = self.province_repo.get_by_attributes(data)
        resources = self.province_repo.dump(provinces.items, True)

        return dict(provinces=resources, total=provinces.total), [], SUCCESS

    def create_provinces(self, data):
        """Create new Provinces

        TODO: add validation rules and give a proper status

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        self.province_repo.bulk_add(data)

        return 'added provinces', [], SUCCESS

    def get_city(self, city_id):
        """Get a specific city using the its ID

        Args:
            city_id: an id for the resource

        Returns:
            a resource, errors, and the status
        """
        city = self.city_repo.get_by_id(city_id)

        resource = self.city_repo.dump(city)
        return dict(city=resource), [], SUCCESS

    def get_cities(self, data):
        """Get a list of city, can be filtered using the allowed filters

        Args:
            data: an object which holds the information of the request

        Returns:
            a resources, errors, and the status
        """
        validator = Validator(self.get_validation_schema, allow_unknown=True)
        validator.validate(data, self.get_validation_schema)

        if validator.errors:
            return [], validator.errors, ERROR

        cities = self.city_repo.get_by_attributes(data)
        resources = self.city_repo.dump(cities.items, True)

        return dict(cities=resources, total=cities.total), [], SUCCESS

    def create_cities(self, data):
        """Create new cities

        TODO: add validation rules and give a proper status

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        self.city_repo.bulk_add(data)

        return 'added cities', [], SUCCESS

    def get_district(self, district_id):
        """Get a specific district using the its ID

        Args:
            district_id: an id for the resource

        Returns:
            a resource, errors, and the status
        """
        district = self.district_repo.get_by_id(district_id)
        resource = self.district_repo.dump(district, True)
        return dict(district=resource), [], SUCCESS

    def get_districts(self, data):
        """Get a list of district, can be filtered using the allowed filters

        Args:
            data: an object which holds the information of the request

        Returns:
            a resources, errors, and the status
        """
        validator = Validator(self.get_validation_schema, allow_unknown=True)
        validator.validate(data, self.get_validation_schema)

        if validator.errors:
            return [], validator.errors, ERROR

        districts = self.district_repo.get_by_attributes(data)
        resources = self.district_repo.dump(districts.items, True)

        return dict(districts=resources, total=districts.total), [], SUCCESS

    def create_districts(self, data):
        """Create new districts

        TODO: add validation rules and give a proper status

        Args:
            data: an object which holds the information of the request

        Returns:
            a resource, errors, and the status
        """
        self.district_repo.bulk_add(data)

        return 'added districts', [], SUCCESS
