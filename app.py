#!/usr/bin/env pypy3
# -- coding: utf-8 --
import json
import pymysql
from flask import Flask
from . import *

SSL = True

app = Flask(__name__)
app.debug = True  # ONLY TO DEBUG #
app.response_class = JsonResponse
context = ('/etc/letsencrypt/live/nanobot.tk/fullchain.pem', "/etc/letsencrypt/live/nanobot.tk/privkey.pem")

app.register_blueprint(auth)
app.register_blueprint(files)
app.register_blueprint(profile)
app.register_blueprint(test)

db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


def rerror(ex, status_code=400):  # response error
    r = JsonResponse()
    r.status_code = status_code
    ex_type = type(ex)

    if ex_type == Exception:
        name = ex_type.__name__,
        msg = str(ex)
    elif ex_type == str:
        name = "ValueError",
        msg = ex
    else:
        raise ValueError("'ex' argument must be 'str' or 'Exception'")

    r.data = json.dumps({
        'error': name,
        'message': msg
    })
    return r


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context)
#    app.run(host="0.0.0.0",port=7000)
