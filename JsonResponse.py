from flask import Response


class JsonResponse(Response):
    default_mimetype = 'application/json; charset=utf-8'
