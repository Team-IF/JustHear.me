#!/usr/bin/env pypy3
from flask import Flask, Response, request
import pymysql
import uuid
import json
import bcrypt

context = ("/etc/letsencrypt/live/nanobot.tk/fullchain.pem", "/etc/letsencrypt/live/nanobot.tk/privkey.pem")
app = Flask(__name__)
db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


def on_json_loading_failed_return_dict(e):
    return {}


@app.route('/profile/<uuid>', methods=['get'])
def profile_get(uuid):
    cursor.execute("SELECT * from user_data where uuid=%s", uuid)
    data = cursor.fetchall()[0]
    data['birthday'] = data['birthday'].strftime('%Y%m%d')
    return Response(json.dumps(data), mimetype='application/json; charset=utf-8')


@app.route('/login', methods=['post'])
def login():
    request.on_json_loading_failed = on_json_loading_failed_return_dict
    if request.json.get('email') is None or request.json.get('pass') is None:
        res = Response()
        res.status_code = 400
        return res
    else:
        cursor.execute("SELECT * from user_data where email=%s",request.json.get('email'))
        data = cursor.fetchall()[0]
        if bcrypt.checkpw(request.json.get('pass').encode('utf-8'),data.get['pass']):
            res = Response()
            res.status_code = 200
            res.data = data['uuid']
            return res
        else:
            res = Response()
            res.status_code = 403
            return res

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context)
#    app.run(host="0.0.0.0",port=7000)
