import csv

"""
    'info' : {
        '{province_key}': {
            {attrs_key}: {attrs_value},
            cities: {}
        }
    }
"""
info = {}
with open('./data/provinces_cleaned.csv', mode='r') as provinces_file:
    provinces_reader = csv.DictReader(provinces_file)

    for province in provinces_reader:
        name = province['name'].lower()
        name = name.replace(' ', '_')
        name = name.replace('-', '_')
        raw_province = {
            'id': province['id'],
            'name': name,
            'is_pickup_available': province['is_pickup_available'],
            'cities': {}
        }
        info[name] = raw_province

with open('./data/cities.csv', mode='r') as cities_file:
    cities_reader = csv.DictReader(cities_file)

    for cities in cities_reader:
        name = cities['name'].lower()
        name = name.replace(' ', '_')
        name = name.replace('-', '_')
        raw_city = {
            'id': cities['id'],
            'name': name,
            'is_pickup_available': cities['is_pickup_available']
        }
        info[cities['province_id']]['cities'][name] = raw_city

op = open('./data/districts.csv', 'r')
dt = csv.DictReader(op)
up_dt = []
counter = 0
not_found = 0
not_found_list = []
for r in dt:
    sel_info = info[r['province_name']]['cities'].get(r['city_name'], '')
    if sel_info == '':
        not_found += 1
        if r['city_name'] not in not_found_list:
            not_found_list.append(r['city_name'])
        continue
    is_pickup_available = 'F'
    if sel_info.get('is_pickup_available', '') == 'T':
        is_pickup_available = 'T'
    counter += 1
    row = {
            'id': counter,
            'city_id': sel_info.get('id'),
            'name': r['name'],
            'postal_code': r['postal_code'],
            'is_pickup_available': is_pickup_available
           }
    up_dt.append(row)

op.close()
op = open('./data/districts_cleaned.csv', 'w', newline='')
headers = ['id', 'city_id', 'name', 'postal_code', 'is_pickup_available']
data = csv.DictWriter(op, delimiter=',', fieldnames=headers)
data.writerow(dict((heads, heads) for heads in headers))
data.writerows(up_dt)

op.close()
# Mountain province, cities are not crawled
# ['barlig', 'bauko', 'besao', 'bontoc', 'natonin', 'paracelis', 'sabangan', 'sadanga', 'sagada', 'tadian', '
# bacolod_city', 'bago_city', 'binalbagan', 'cadiz_city', 'calatrava', 'candoni']