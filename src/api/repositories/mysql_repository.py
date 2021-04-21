from flask import abort
from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from typing import Any, List, Dict
from src.extensions import database


class MySQLRepository:
    def __init__(self) -> None:
        self._model: Any = object
        self.schema: Any = object
        self.schemas: Any = object
        self.schema_to_many: Any = object
        self._data: Any = []
        self._attr_id: str = ''
        self.default_sort_key: str = ''
        self.allowed_sort_keys = []
        self.allowed_filter_keys = []
        self.creatable_fields = []
        self.updatable_fields = []

    def get_by_id(self, field_id: int) -> Any:
        self.find_by_id(field_id)
        return self._data

    def add(self, payload: Any) -> Any:
        self._data = self._model(**payload)
        try:
            database.session.add(self._data)
            database.session.commit()
            database.session.flush()

            return self._data
        except SQLAlchemyError as error:
            abort(400, str(error.__dict__['orig']))

            return False

    def get_all(self) -> Any:
        return self._model.query.all()

    def find_by_id(self, field_id: int) -> None:
        data = self._model.query.filter_by(**{self._attr_id: field_id}).first()
        self._data = data

        return self._data

    def find_all_by_id(self, field_id: int) -> None:
        self._data = self._model.query.filter_by(**{self._attr_id: field_id})

        return self._data

    def update(self, field_id: int, payload: Any) -> Any:
        self.find_by_id(field_id)

        for key in payload.keys():
            setattr(self._data, key, payload[key])

        database.session.commit()

        return self._data

    def delete_by_id(self, field_id: int) -> Any:
        self.find_by_id(field_id)
        database.session.delete(self._data)
        database.session.commit()

        return field_id

    # Bulk add to scylladb
    def bulk_add(self, payloads: list) -> Any:
        data: list = [self._model(**payload) for payload in payloads]
        database.session.bulk_save_objects(data)
        database.session.commit()

        return data

    # Bulk update
    def bulk_update(self, payloads: list) -> Any:
        database.session.bulk_update_mappings(self._model, payloads)
        database.session.commit()

        return payloads

    def get_by_attributes(self, data: Any) -> Any:
        order_by = self.get_order_by(data)
        filters = MySQLRepository.get_filters(self.allowed_filter_keys, data)
        pagination = MySQLRepository.get_pagination(data)
        resources = None

        try:
            resources = self._model \
                .query \
                .filter_by(**filters) \
                .order_by(order_by) \
                .paginate(**pagination, error_out=False)
        except InvalidRequestError:
            database.session.rollback()
        # Investigate the .order_by(order_by) \

        return resources

    def get_by_attributes_first(self, filter_keys: List, data: Any, verify_password: bool = False) -> Any:
        filters = MySQLRepository.get_filters(filter_keys, data)

        # Disallow empty filters
        if len(filters) == 0:
            return False

        result = self._model\
            .query\
            .filter_by(**filters)\
            .first()

        # Option to verify the model using the given password, make sure that the model has a check_password method
        if result and verify_password:
            password = data.get('password', '')
            is_matched = self._model.check_password(result.password, password)
            if is_matched:
                return result
            return False

        return result

    # Delete by attributes
    def delete_by_attributes(self, attributes: Dict[str, Any]) -> Any:
        result = self.get_by_attributes(attributes, False)
        database.session.delete(result)
        database.session.commit()

        return attributes

    def dump(self, data: any, is_many=False) -> Any:
        if is_many and type(data) == list:
            return [self.schema.dump(item) for item in data]

        return self.schema.dump(data)

    @staticmethod
    def get_filters(allowed_filter_keys: List, data: any):
        filters = dict()
        for key in allowed_filter_keys:
            if key in data:
                filters[key] = data.get(key)

        return filters

    def get_order_by(self, data: any):
        sort_key = data.get('sort_by', self.default_sort_key)
        sort_order = data.get('sort_order', 'desc')

        if sort_key not in self.allowed_sort_keys:
            sort_key = self.default_sort_key

        sort_order_keys = ['asc', 'desc']
        sort_order = sort_order.lower()
        if sort_order not in sort_order_keys:
            sort_order = 'desc'

        order_by = getattr(self._model, sort_key).desc()
        if sort_order == 'asc':
            order_by = getattr(self._model, sort_key).asc()

        return order_by

    @staticmethod
    def get_pagination(data):
        # 1 as default
        page = MySQLRepository.str_to_int(data.get('page', 1), 1)
        page = 1 if page == 0 or page > 500 else page

        # 100 as default
        per_page = MySQLRepository.str_to_int(data.get('limit', 100), 100)
        per_page = 100 if per_page > 1000 else per_page

        return dict(page=page, per_page=per_page)

    @staticmethod
    def str_to_int(value: any, default_value):
        if type(value) == str:
            if value.isnumeric():
                value = int(value)
            else:
                value = default_value

        return value
