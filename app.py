#!/usr/bin/env pypy3
import json
import uuid
import datetime
import bcrypt
import pymysql
from flask import Flask, Response, request

context = ('/etc/letsencrypt/live/nanobot.tk/fullchain.pem', "/etc/letsencrypt/live/nanobot.tk/privkey.pem")
app = Flask(__name__)
db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def on_json_loading_failed_return_dict(e):
    return {}


@app.route('/profile/<uuidd>', methods=['get'])
def profile_get(uuidd):
    cursor.execute("SELECT * from user_data where uuid=%s", uuidd)
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
        cursor.execute("SELECT * from user_data where email=%s", request.json.get('email'))
        data = cursor.fetchall()[0]
        if bcrypt.checkpw(request.json.get('pass').encode('utf-8'), data.get('pass').encode('utf-8')):
            newtoken = str(uuid.uuid4())
            expiredate = datetime.datetime.utcnow()
            expiredate = expiredate + datetime.timedelta(days=14)
            cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ", (data['uuid'], newtoken, expiredate))
            res = Response()
            res.status_code = 200
            res.data = newtoken
            return res
        else:
            res = Response()
            res.status_code = 403
            return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context)
#    app.run(host="0.0.0.0",port=7000)
