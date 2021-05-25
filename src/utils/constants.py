ERROR = 'error' # internal errors
FAILURE = 'failure' # operation errors
SUCCESS = 'success' # operation success


VALIDATION_ERROR = 'validation errors'
SERVER_ERROR = 'server errors'

DELIVERY_CREATION_FAILED = 'failed to create delivery'
DELIVERY_CREATION_SUCCESS = 'delivery successfully created'
DELIVERY_UPDATE_FAILED = 'failed to update delivery'
DELIVERY_UPDATE_SUCCESS = 'delivery successfully updated'

MANILA_PROVINCE_ID = [49]
GREATER_MANILA_PROVINCE_ID = [17, 24, 42, 65]
GREATER_MANILA_CITY_ID = [280, 282, 283, 290, 291, 299, 302, 416, 418, 419, 420, 422, 423, 434, 773, 776, 1319, 1322,
                          1328, 1130]

# Labels:
# greater_manila to manila (gm_to_m)
# greater_manila to greater_manila (gm_to_gm)
# greater_manila to luzon, visayas, mindanao (gm_to_lvm)
# manila to manila (m_to_m)
# manila to greater_manila (m_to_gm)
# manila to luzon, visayas, mindanao (m_to_lvm)
# SHIPPING_FEES = {
#     'S': {
#         'gm_to_m': {
#             'fee': 120
#         },
#         'gm_to_gm': {
#             'fee': 100
#         },
#         'gm_to_lvm': {
#             'fee': 200
#         },
#         'm_to_m': {
#             'fee': 100
#         },
#         'm_to_gm': {
#             'fee': 120
#         },
#         'm_to_lvm': {
#             'fee': 200
#         }
#     },
#     'M': {
#         'gm_to_m': {
#             'fee': 150
#         },
#         'gm_to_gm': {
#             'fee': 150
#         },
#         'gm_to_lvm': {
#             'fee': 250
#         },
#         'm_to_m': {
#             'fee': 120
#         },
#         'm_to_gm': {
#             'fee': 150
#         },
#         'm_to_lvm': {
#             'fee': 230
#         }
#     },
#     'L': {
#         'gm_to_m': {
#             'fee': 180
#         },
#         'gm_to_gm': {
#             'fee': 180
#         },
#         'gm_to_lvm': {
#             'fee': 300
#         },
#         'm_to_m': {
#             'fee': 150
#         },
#         'm_to_gm': {
#             'fee': 180
#         },
#         'm_to_lvm': {
#             'fee': 300
#         }
#     },
#     'B': {
#         'gm_to_m': {
#             'fee': 200
#         },
#         'gm_to_gm': {
#             'fee': 200
#         },
#         'gm_to_lvm': {
#             'fee': 0
#         },
#         'm_to_m': {
#             'fee': 200
#         },
#         'm_to_gm': {
#             'fee': 220
#         },
#         'm_to_lvm': {
#             'fee': 470
#         }
#     },
#     'OWN': {
#         'gm_to_m': {
#             'fee': 220
#         },
#         'gm_to_gm': {
#             'fee': 220
#         },
#         'gm_to_lvm': {
#             'fee': 500
#         },
#         'm_to_m': {
#             'fee': 180
#         },
#         'm_to_gm': {
#             'fee': 200
#         },
#         'm_to_lvm': {
#             'fee': 0
#         }
#     }
# }

SHIPPING_FEES = {
    'S': {
        'metro_manila': {
            'fee': 80
        },
        'greater_manila': {
            'fee': 150
        },
        'luzon': {
            'fee': 190
        },
        'visayas': {
            'fee': 210
        },
        'mindanao': {
            'fee': 230
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
            'fee': 220
        },
        'visayas': {
            'fee': 240
        },
        'mindanao': {
            'fee': 260
        }
    },
    'L': {
        'metro_manila': {
            'fee': 180
        },
        'greater_manila': {
            'fee': 210
        },
        'luzon': {
            'fee': 280
        },
        'visayas': {
            'fee': 300
        },
        'mindanao': {
            'fee': 320
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

response = {
    'status': '',
    'data': {

    },
    'message': '',
    'errors': {

    }
}
