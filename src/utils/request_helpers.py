from flask import request


def get_request_data(req: request, **kwargs):
    data = req.json if req.json else {}
    data.update(req.args)
    data.update(kwargs)

    return data

# def get_request_data(req: request, **kwargs):
#     locations = {}
#     data = {}
#     data.update(req.args)
#     data.update(kwargs)
#     # locations.update(dict(zip(req.args.keys(), ['url'] * len(req.args.keys()))))
#     # locations.update(dict(zip(kwargs.keys(), ['path'] * len(kwargs.keys()))))
#     data = req.json if req.json else {}
#     if req.json:
#         locations.update(dict(zip(req.json.keys(), ['body'] * len(req.json.keys()))))
#
#     return data
