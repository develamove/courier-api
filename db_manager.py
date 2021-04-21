from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from src.extensions import database
from app import create_app
from src.api.services.location import LocationService
import csv

app = create_app()
manager = Manager(app)
migrate = Migrate(app, database)
manager.add_command('db', MigrateCommand)

location_service = LocationService()


@manager.command
def create_provinces():
    with open('./data/provinces.csv', mode='r') as provinces_file:
        provinces_reader = csv.DictReader(provinces_file)
        provinces = []
        for province in provinces_reader:
            raw_province = {
                'name': province['name'],
                'is_pickup_available': province['is_pickup_available']
            }
            provinces.append(raw_province)
        result = location_service.create_provinces(provinces)


@manager.command
def create_cities():
    provinces, _, _ = location_service.get_provinces()
    provinces_keys = {}
    for province in provinces:
        raw_province = {}
        province_name = province['name'].lower()
        province_name = province_name.replace(' ', '_')
        province_name = province_name.replace('-', '_')
        raw_province[province_name] = province
        provinces_keys.update(raw_province)

    with open('./data/cities.csv', mode='r') as cities_file:
        cities_file = csv.DictReader(cities_file)
        cities = []
        for city in cities_file:
            raw_city = {
                'province_id': provinces_keys[city['province_name']]['id'],
                'name': city['name'],
                'is_pickup_available': city['is_pickup_available']
            }
            cities.append(raw_city)

        result = location_service.create_cities(cities)


@manager.command
def create_districts():
    cities_keys = {}
    city_counter =0
    for counter in range(1, 20):
        filters = {
            'page': counter,
            'limit': 100
        }
        cities, _, _ = location_service.get_cities(filters)
        cached_province_id = 0
        cached_province = None
        for city in cities['cities']:
            raw_city = {}
            city_name = city['name'].lower()
            city_name = city_name.replace(' ', '_')
            city_name = city_name.replace('-', '_')

            if cached_province_id != city['province_id']:
                province, _, _ = location_service.get_province(city['province_id'])
                cached_province = province
                cached_province_id = city['province_id']
            province_name = cached_province['name'].lower()
            province_name = province_name.replace(' ', '_')
            province_name = province_name.replace('-', '_')
            raw_city[str(province_name + '_' + city_name)] = city
            city_counter += 1
            cities_keys.update(raw_city)

    with open('./data/districts.csv', mode='r') as districts_file:
        districts_file = csv.DictReader(districts_file)
        districts = []
        cached_city_name = ''
        is_cached = True
        for district in districts_file:
            city_key = district['province_name'] + '_' + district['city_name']

            if is_cached:
                is_cached = False
                cached_city_name = city_key

            raw_city = {
                'city_id': cities_keys[city_key]['id'],
                'name': district['name'],
                'postal_code': district['postal_code'],
                'is_pickup_available': district['is_pickup_available']
            }

            if cached_city_name != city_key:
                result = location_service.create_districts(districts)
                districts = []

            districts.append(raw_city)

# Commands
# python db_manager.py db init
# python db_manager.py db migrate
# python db_manager.py db stamp head (if ERROR [flask_migrate] Error: Target database is not up to date. occurs)
# python db_manager.py db upgrade


if __name__ == '__main__':
    manager.run()
