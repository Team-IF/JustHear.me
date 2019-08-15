#!/usr/bin/env pypy3
from flask import Flask, Response
import pymysql
import uuid
import json
import datetime

context = ("/etc/letsencrypt/live/nanobot.tk/fullchain.pem","/etc/letsencrypt/live/nanobot.tk/privkey.pem")
app = Flask(__name__)
db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock",user="hearme",password="dhdh4321",db="hearme",charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


@app.route('/profile/<uuid>', methods=['get'])
def profile_get(uuid):
    cursor.execute(f"SELECT * from user_data where uuid='{uuid}'")
    data = cursor.fetchall()
    data = data[0]
    data['birthday'] = data['birthday'].strftime('%Y%m%d')
    return Response(json.dumps(data), mimetype='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6000,ssl_context=context)
