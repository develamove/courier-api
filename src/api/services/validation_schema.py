base_fetch_schema = {
    'sort_by': {
        'type': 'string'
    },
    'sort_order': {
        'type': 'string'
    },
}

fetch_staff_schema = base_fetch_schema
register_staff_schema = {
    'username': {
        'type': 'string',
        'required': False,
        'empty': False
    },
    'password': {
        'type': 'string',
        'required': True,
        'empty': False
    },
     'role': {
        'type': 'string',
        'required': True,
        'allowed': ['ADMIN', 'admin']
    }
}

fetch_client_schema = base_fetch_schema
register_client_schema = {
        'username': {
            'type': 'string',
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 30
        },
        'password': {
            'type': 'string',
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 30
        },
        'first_name': {
            'type': 'string',
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 40
        },
        'middle_name': {
            'type': 'string',
            'maxlength': 30
        },
        'last_name': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 3,
            'maxlength': 40
        },
        'email': {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'minlength': 3,
            'maxlength': 40
        },
        'cellphone_no': {
            'type': 'string',
        },
        'province': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 50
        },
        'city': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 50
        },
        'district': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 50
        },
        'landmarks': {
            'type': 'string'
        }
    }
modify_client_schema = {
        # 'username': {
        #     'type': 'string',
        #     'required': False
        # },
        # 'password': {
        #     'type': 'string',
        #     'required': True
        # },
        'first_name': {
            'type': 'string',
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 40
        },
        'middle_name': {
            'type': 'string',
            'minlength': 3,
            'maxlength': 30
        },
        'last_name': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 3,
            'maxlength': 40
        },
        'email': {
            'type': 'string',
            'empty': False,
            'required': True,
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'minlength': 3,
            'maxlength': 40
        },
        'cellphone_no': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 11,
            'maxlength': 13
        },
        'province': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 5,
            'maxlength': 50
        },
        'city': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 5,
            'maxlength': 50
        },
        'district': {
            'type': 'string',
            'empty': False,
            'required': True,
            'minlength': 5,
            'maxlength': 50
        },
        'landmarks': {
            'type': 'string'
        }
    }

fetch_delivery_schema = base_fetch_schema
fetch_delivery_status_schema = base_fetch_schema
create_delivery_schema = {
        'receipt_id': {
            'type': 'string',
            'empty': False,
            'maxlength': 15
        },
        'item_type': {
            'type': 'string',
            'empty': False,
            'required': True,
            'allowed': ['S', 'M', 'L', 'B']
        },
        'item_description': {
            'type': 'string',
            'empty': False,
            'required': True,
            'maxlength': 50
        },
        'item_value': {
            'type': 'integer',
            'min': 0,
            'max': 1000000
        },
        'payment_method': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['cod', 'regular']
        },
        'service_fees_payor': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['sender', 'recipient']
        },
        'sender': {
            'type': 'dict',
            'required': True,
            'schema': {
                'province_id': {
                    'type': 'integer',
                    'required': True,
                    'empty': False
                },
                'full_name': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'cellphone_no': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'minlength': 11,
                    'maxlength': 13,
                    # 'check_cp_format': True
                },
                'province': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'city': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'district': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'street': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'landmarks': {
                    'type': 'string',
                    'maxlength': 50
                },
                'postal_code': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 15
                }
            }
        },
        'recipient': {
            'type': 'dict',
            'required': True,
            'schema': {
                'province_id': {
                    'type': 'integer',
                    'required': True,
                    'empty': False
                },
                'full_name': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'cellphone_no': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'minlength': 11,
                    'maxlength': 13
                },
                'province': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'city': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'district': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'street': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 50
                },
                'landmarks': {
                    'type': 'string',
                    'maxlength': 50
                },
                'postal_code': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'maxlength': 15
                }
            }
        }
    }
modify_delivery_schema = {
        'is_cod': {
            'type': 'string',
            'empty': False,
            'allowed': ['F', 'T']
        },
        'is_provincial': {
            'type': 'string',
            'empty': False,
            'allowed': ['F', 'T']
        },
        'item_name': {
            'type': 'string',
            'empty': False,
            'maxlength': 50
        },
        'item_type': {
            'type': 'string',
            'empty': False,
            'allowed': ['S', 'M', 'L', 'XL', 'B']
        },
        'item_amount': {
            'type': 'integer',
            'empty': False,
        },
        'item_weight': {
            'type': 'integer',
            'empty': False,
            'min': 1,
            'max': 100
        },
        'total_amount': {
            'type': 'integer',
            'empty': False,
        },
        'sender': {
            'type': 'dict',
            'schema': {
                'full_name': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'cellphone_no': {
                    'type': 'string',
                    'empty': False,
                    'minlength': 11,
                    'maxlength': 13,
                    'check_with': 'cp_no_format'
                },
                'province': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'city': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'district': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'street': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'landmarks': {
                    'type': 'string',
                    'maxlength': 50
                },
                'postal_code': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 15
                }
            }
        },
        'recipient': {
            'type': 'dict',
            'schema': {
                'full_name': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'cellphone_no': {
                    'type': 'string',
                    'empty': False,
                    'minlength': 11,
                    'maxlength': 13,
                    'check_with': 'cp_no_format'
                },
                'province': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'city': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'district': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'street': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 50
                },
                'landmarks': {
                    'type': 'string',
                    'maxlength': 50
                },
                'postal_code': {
                    'type': 'string',
                    'empty': False,
                    'maxlength': 15
                }
            }
        }
    }

create_event_schema = {
    'name': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['for_pickup', 'picked_up', 'in_transit', 'failed', 'delivered', 'cancelled', 'remitted']
    },
    'remarks': {
        'type': 'string',
        'maxlength': 100
    }
}
