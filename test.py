# to test blueprint module and server

from flask import Blueprint, request
import app

test = Blueprint('test', __name__)


@test.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo():
    return request.data.decode("utf-8")


@test.route('/error', methods=['GET'])
def error():
    return app.rerror('test error', 400)
