from flask import Blueprint, request
from src.api.services.location import LocationService
from src.utils import response_creator, get_request_data

loc_service = LocationService()
locations = Blueprint('Locations', __name__, url_prefix='/locations')


@locations.route('/provinces/<province_id>')
@response_creator
def get_province(province_id):
    return loc_service.get_province(province_id)


@locations.route('/provinces')
@response_creator
def get_provinces():
    data = get_request_data(request)
    return loc_service.get_provinces(data)


@locations.route('/provinces', methods=['POST'])
@response_creator
def create_provinces():
    data = get_request_data(request)
    return loc_service.create_provinces(data)


@locations.route('/cities/<city_id>/')
@response_creator
def get_city(city_id):
    return loc_service.get_city(city_id)


@locations.route('/cities')
@response_creator
def get_cities():
    data = get_request_data(request)
    return loc_service.get_cities(data)


@locations.route('/cities', methods=['POST'])
@response_creator
def create_cities():
    data = get_request_data(request)
    return loc_service.create_cities(data)


@locations.route('/districts/<district_id>/')
@response_creator
def get_district(district_id):
    return loc_service.get_district(district_id)


@locations.route('/districts')
@response_creator
def get_districts():
    data = get_request_data(request)
    return loc_service.get_districts(data)


@locations.route('/districts', methods=['POST'])
@response_creator
def create_districts():
    data = get_request_data(request)
    return loc_service.create_districts(data)