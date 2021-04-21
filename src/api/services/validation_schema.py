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
        'client_id': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'receipt_id': {
            'type': 'string',
            'empty': False,
            'maxlength': 30
        },
        'is_cod': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['F', 'T']
        },
        'is_provincial': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['F', 'T']
        },
        'item_name': {
            'type': 'string',
            'empty': False,
            'required': True,
            'maxlength': 50
        },
        'item_type': {
            'type': 'string',
            'empty': False,
            'required': True,
            'allowed': ['S-M', 'S', 'M', 'L', 'XL']
        },
        'item_amount': {
            'type': 'integer',
            'required': True,
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
            'required': True,
            'empty': False,
        },
        'sender': {
            'type': 'dict',
            'required': True,
            'schema': {
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
        'client_id': {
            'required': True,
            'empty': False,
        },
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
            'allowed': ['S-M', 'S', 'M', 'L', 'XL']
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
