from cerberus import Validator


class CustomValidator(Validator):
    def _check_with_cp_no_format(self, field, value):
        """Checks if the cellphone number format is followed (PH cellphone number format)

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        if not self._is_valid_cp_format(value):
            self._error(field, "Invalid cellphone number format.")

    def _is_valid_cp_format(self, cp_no: str) -> bool:
        cp_no_list = list(cp_no)

        if cp_no_list[0:2] == ['0', '9'] and len(cp_no_list) == 11:
            return True

        if cp_no_list[0:3] == ['6', '3', '9'] and len(cp_no_list) == 12:
            return True

        if cp_no_list[0:4] == ['+', '6', '3', '9'] and len(cp_no_list) == 13:
            return True

        return False
