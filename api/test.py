# to test blueprint module and server

import JsonResponse
from flask import Blueprint, request
from api import common

test = Blueprint('test', __name__)


@test.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo():
    return request.data.decode("utf-8")


@test.route('/error', methods=['GET'])
def error():
    return common.rerror('test error', 400)
