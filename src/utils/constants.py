# Internal errors
ERROR = 'error'

# Operation errors
FAILURE = 'failure'

# Operation success
SUCCESS = 'success'

# Error messages
VALIDATION_ERROR = 'validation errors'
SERVER_ERROR = 'server errors'
DELIVERY_CREATION_FAILED = 'failed to create delivery'
DELIVERY_CREATION_SUCCESS = 'delivery successfully created'
DELIVERY_UPDATE_FAILED = 'failed to update delivery'
DELIVERY_UPDATE_SUCCESS = 'delivery successfully updated'

# Response format
response = {
    'status': '',
    'data': {},
    'message': '',
    'errors': {}
}

# Locations ID
MANILA_PROVINCE_ID = [
    49
]
GREATER_MANILA_PROVINCE_ID = [
    17,
    24,
    42,
    65
]
GREATER_MANILA_CITY_ID = [
    280,
    282,
    283,
    290,
    291,
    299,
    302,
    416,
    418,
    419,
    420,
    422,
    423,
    434,
    773,
    776,
    1319,
    1322,
    1328,
    1130
]

# Shipping rates
SHIPPING_FEES = {
    'S': {
        'metro_manila': {
            'fee': 80
        },
        'greater_manila': {
            'fee': 150
        },
        'luzon': {
            'fee': 170
        },
        'visayas': {
            'fee': 170
        },
        'mindanao': {
            'fee': 170
        }
    },
    'M': {
        'metro_manila': {
            'fee': 120
        },
        'greater_manila': {
            'fee': 180
        },
        'luzon': {
            'fee': 200
        },
        'visayas': {
            'fee': 200
        },
        'mindanao': {
            'fee': 200
        }
    },
    'L': {
        'metro_manila': {
            'fee': 150
        },
        'greater_manila': {
            'fee': 210
        },
        'luzon': {
            'fee': 250
        },
        'visayas': {
            'fee': 250
        },
        'mindanao': {
            'fee': 250
        }
    },
    'B': {
        'metro_manila': {
            'fee': 220
        },
        'greater_manila': {
            'fee': 300
        },
        'luzon': {
            'fee': 470
        },
        'visayas': {
            'fee': 500
        },
        'mindanao': {
            'fee': 550
        }
    }
}
