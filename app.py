#!/usr/bin/env pypy3
import datetime
import json
from uuid import uuid4

import bcrypt
import pymysql
from flask import Flask, Response, request

context = ('/etc/letsencrypt/live/nanobot.tk/fullchain.pem', "/etc/letsencrypt/live/nanobot.tk/privkey.pem")
app = Flask(__name__)
db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


def token2uuid(token: str) -> str:
    cursor.execute("SELECT * from sessions where accessToken=%s", token)
    uuid = cursor.fetchall()[0]['uuid']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    cursor.execute("UPDATE 'sessions' SET expiredate=%s WHERE accessToken=%s", (expiredate, token))
    db.commit()
    return uuid


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def on_json_loading_failed_return_dict(e):
    return {}


@app.route('/profile/<token>', methods=['get'])
def profile_get(token):
    uuid = token2uuid(token)
    cursor.execute("SELECT * from user_data where uuid=%s", uuid)
    data = cursor.fetchall()[0]
    data['birthday'] = data['birthday'].strftime('%Y%m%d')
    del data['uuid'], data['pass']
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
            newtoken = str(uuid4())
            expiredate = datetime.datetime.utcnow()
            expiredate = expiredate + datetime.timedelta(days=14)
            cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ", (data['uuid'], newtoken, expiredate))
            db.commit()
            res = Response()
            res.status_code = 200
            res.data = newtoken
            res.mimetype = 'text/plain; charset=utf-8'
            return res
        else:
            res = Response()
            res.status_code = 403
            return res


@app.route('/login/<token>', methods=['DELETE'])
def invalidate_token(token: str):
    cursor.execute("DELETE FROM sessions WHERE accessToken=%s", token)
    db.commit()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context)
#    app.run(host="0.0.0.0",port=7000)
