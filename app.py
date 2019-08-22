#!/usr/bin/env pypy3
# -- coding: utf-8 --
import datetime
import json
from uuid import uuid4

import bcrypt
import pymysql
from flask import Flask, Response, request

from JsonResponse import JsonResponse

context = ('/etc/letsencrypt/live/nanobot.tk/fullchain.pem', "/etc/letsencrypt/live/nanobot.tk/privkey.pem")
app = Flask(__name__)
app.debug = True  # ONLY TO DEBUG #
app.response_class = JsonResponse
db = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                     charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)

x_access_token = "x-access-token"


# token to uuid
# TODO : check client ip and compare with db
# TODO : change token format to more random string
def token2uuid(token: str) -> str:
    cursor.execute("SELECT * from sessions where accessToken=%s", token)
    fetchs = cursor.fetchall()

    if not fetchs or len(fetchs) == 0:
        raise ValueError("Invalid Token")

    uuid = fetchs[0]['uuid']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    cursor.execute("UPDATE 'sessions' SET expiredate=%s WHERE accessToken=%s", (expiredate, token))
    db.commit()
    return uuid


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def get_profile(uuid: str):
    cursor.execute("SELECT * from user_data where uuid=%s", uuid)
    fetchs = cursor.fetchall()

    if not fetchs or len(fetchs) == 0:
        raise ValueError("해당 유저를 찾을 수 없습니다.")

    data = fetchs[0]
    data['birthday'] = data['birthday'].strftime('%Y-%m-%d')
    del data['uuid'], data['pass']
    return data


# GET someone's profile
@app.route('/profile/<uuid>', methods=['get'])
def profile_get(uuid: str) -> Response:
    try:
        profile = get_profile(uuid)
        return json.dumps(profile)

    except ValueError as e:  # can't find user
        return rerror(e, 404)

    except Exception as e:  # other error
        return rerror(e, 500)


# EDIT my profile (계정주인만 수정가능)
@app.route('/profile/<uuid>', methods=['put'])
def profile_edit(uuid: str) -> Response:
    try:
        token = request.headers[x_access_token]

        if not token:
            return rerror("로그인을 해주세요.", 401)
        if uuid != token2uuid(token):
            return rerror("자신의 프로필만 수정할 수 있습니다.", 403)

        args = json.loads(request.data)
        if 'username' in args:
            pass
        if 'email' in args:
            pass
        if 'phonenumber' in args:
            pass
        if 'birthday' in args:
            pass
        if 'gender' in args:
            pass
        if 'profileImg' in args:
            pass
        if 'profileMusic' in args:
            pass

        return json.dumps(get_profile(uuid))

    except json.JSONDecodeError as e:
        return rerror(e, 400)
    except Exception as e:
        return rerror(e, 500)


# LOGIN
# TODO : check email and pw validation
@app.route('/login', methods=['post'])
def login() -> Response:
    try:
        req = json.loads(request.data)
        if not req.get('email') or not req.get("pw"):
            return rerror("이메일과 비밀번호를 입력해 주세요.", 400)

        cursor.execute("SELECT * from user_data where email=%s", request.json.get('email'))
        fetchs = cursor.fetchall()

        if not fetchs or len(fetchs) == 0:
            return rerror("잘못된 이메일/비밀번호", 403)

        data = fetchs[0]
        if bcrypt.checkpw(request.json.get('pass').encode('utf-8'), data.get('pass').encode('utf-8')):
            newtoken = str(uuid4())
            expiredate = datetime.datetime.utcnow()
            expiredate = expiredate + datetime.timedelta(days=14)
            cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ", (data['uuid'], newtoken, expiredate))
            db.commit()
            return JsonResponse(json.dumps({
                'token': newtoken,
                'uuid': data['uuid']
            }))
        else:
            return rerror("잘못된 이메일/비밀번호", 403)

    except json.JSONDecodeError as e:
        return rerror(e)


@app.route('/login', methods=['DELETE'])
def invalidate_token() -> Response:
    try:
        token = request.headers[x_access_token]

        if not token:
            return rerror("로그인을 해주세요.", 403)

        cursor.execute("DELETE FROM sessions WHERE accessToken=%s", token)
        db.commit()
        return Response(status=204)

    except Exception as e:
        return rerror(e)


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
