from sqlalchemy import asc, desc


def get_filters(allowed_keys: list, data: any):
    filters = dict()
    for key in allowed_keys:
        if key in data:
            filters[key] = data.get(key)

    return filters


def get_order_by(model: any, sort_keys: list, default_sort_key: str, data: any):
    sort_key = data.get('sort_by', default_sort_key)
    sort_order = data.get('sort_order', 'desc')

    if sort_key not in sort_keys:
        sort_key = default_sort_key

    sort_order_keys = ['asc', 'desc']
    sort_order = sort_order.lower()
    if sort_order not in sort_order_keys:
        sort_order = 'desc'

    order_by = desc(getattr(model, sort_key))
    if sort_order == 'asc':
        order_by = asc(getattr(model, sort_key))

    return order_by


def get_pagination(data):
    page = str_to_int(data.get('page', 0), 0)
    page = 1 if page == 0 or page > 500 else page

    per_page = str_to_int(data.get('limit', 10), 10)
    per_page = 10 if per_page > 100 else per_page

    return dict(page=page, per_page=per_page)


def str_to_int(value: any, default_value):
    if type(value) == str:
        if value.isnumeric():
            value = int(value)
        else:
            value = default_value

    return value
