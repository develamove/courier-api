from flask import request


def get_request_data(req: request, **kwargs):
    data = req.json if req.json else {}
    data.update(req.args)
    data.update(kwargs)

    return data
