import random
import math
import string
from typing import List, Dict


def create_tracking_id():
    """Create a 12 random string

    Returns:
        a tracking number
    """
    return get_random_str(4).upper() + get_random_digits(8)


def get_random_str(str_len: int):
    random_str = ''

    for counter in range(str_len):
        random_str += random.choice(string.ascii_letters)

    return random_str


def get_random_digits(num_len: int):
    digits = [i for i in range(0, 10)]
    random_str = ''

    for counter in range(num_len):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str


def filter_dict(allowed_list: List, data: Dict):
    filtered_data = {}
    for key in data.keys():
        if key in allowed_list:
            filtered_data[key] = data[key]

    return filtered_data


def format_cp_no(cp_no: str) -> string:
    cp_no_list = list(cp_no)
    empty_cp_no = ''

    if cp_no_list[0:2] == ['0', '9'] and len(cp_no_list) == 11:
        cp_no_list = cp_no_list[2:]
    elif cp_no_list[0:3] == ['6', '3', '9'] and len(cp_no_list) == 12:
        cp_no_list = cp_no_list[3:]
    elif cp_no_list[0:4] == ['+', '6', '3', '9'] and len(cp_no_list) == 13:
        return empty_cp_no.join(cp_no_list)

    return '+639' + empty_cp_no.join(cp_no_list)


class ErrorManager:
    _errors: {}

    def add_error(self, key: str, error: str) -> None:
        if key in self._errors:
            self._errors[key].append(error)

    def get_errors(self) -> object:
        return self._errors

    def clear_errors(self):
        self._errors = {}
        return self

    @staticmethod
    def create_error(key: str, error: any) -> object:
        error_obj = {}

        if type(error) == list:
            error_obj[key] = error
        else:
            error_obj[key] = [error]

        return error_obj
