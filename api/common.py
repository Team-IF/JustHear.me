# -- coding: utf-8 --
import json
import re
import traceback
import uuid

import pymysql

import JsonResponse

SSL = True
emailregex = re.compile('^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$')


class User:
    def __init__(self, uid):
        self.uuid = uuid.UUID(uid)
        pass


def rerror(ex, status_code: int = 400) -> JsonResponse:  # response error
    r = JsonResponse.JsonResponse()
    r.status_code = status_code

    if isinstance(ex, Exception):
        name = type(ex).__name__
        msg = str(ex)
    elif isinstance(ex, str):
        name = "ValueError"
        msg = ex
    else:
        raise ValueError("'ex' argument must be 'str' or 'Exception'")
    traceback.print_exc()
    r.data = json.dumps({
        'error': name,
        'message': msg
    })
    return r


print("Connecting DB...")

db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)

