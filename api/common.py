# -- coding: utf-8 --
import JsonResponse
import json
import traceback
import pymysql
SSL = True

def rerror(ex, status_code=400):  # response error
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

