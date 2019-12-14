import datetime
from uuid import uuid4

import bcrypt
import pymysql
from flask import Blueprint, request, Response

from JsonResponse import JsonResponse
from api import common

# authenticate user

auth = Blueprint('auth', __name__)



# LOGIN
# TODO : check email and pw validation
@auth.route('/login', methods=['post'])
def login() -> JsonResponse:
    try:
        if not request.is_json:
            return common.rerror("invalid json", 400)

        req = request.json
        if not req.get('email') or not req.get("pass"):
            return common.rerror("이메일과 비밀번호를 입력해 주세요.", 400)

        common.cursor.execute("SELECT * from user_data where email=%s", req.get('email'))
        fetchs = common.cursor.fetchall()

        if not fetchs or len(fetchs) == 0:
            return common.rerror("잘못된 이메일/비밀번호", 403)

        data = fetchs[0]
        if bcrypt.checkpw(req.get('pass').encode('utf-8'), data.get('pass').encode('utf-8')):
            newtoken = str(uuid4())
            expiredate = datetime.datetime.utcnow()
            expiredate = expiredate + datetime.timedelta(days=14)
            common.cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ",
                                  (data['uuid'], newtoken, expiredate))
            common.db.commit()
            return JsonResponse({
                'token': newtoken,
                'uuid': data['uuid']
            })
        else:
            return common.rerror("잘못된 이메일/비밀번호", 403)

    except Exception as e:
        return common.rerror(e, 500)


@auth.route('/register', methods=['POST'])
def register() -> JsonResponse:
    try:
        if not request.is_json:
            return common.rerror("invalid json", 400)

        req = request.json
        if not common.emailregex.search(req.get('email')):
            return common.rerror("invalid email", 400)

        common.cursor.execute("select uuid from user_data")
        uuids = common.cursor.fetchall()
        uuids = (x['uuid'] for x in uuids)
        uuid = str(uuid4())
        while uuid in uuids:
            uuid = str(uuid4())

        values = (uuid, req.get('username'), req.get('email'), common.hashpw(req.get('pass')), req.get('phonenumber'),
                  req.get('birthday'), req.get('gender'), req.get('profileImg'), req.get('profileMusic'))

        try:
            common.cursor.execute(
                "INSERT INTO `hearme`.`user_data` (`uuid`, `username`, `email`, `pass`, `phonenumber`, `birthday`, `gender`, `profileImg`, `profileMusic`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                values)
            common.db.commit()
            return Response(status=204)
        except pymysql.IntegrityError as e:
            if 'user_data_email_uindex' in str(e):
                return common.rerror('email is duplicated', 400)
        except Exception as e:
            return common.rerror(e, 500)

    except Exception as e:
        return common.rerror(e, 500)

# delete login token
@auth.route('/login', methods=['DELETE'])
def invalidate_token() -> Response:
    try:
        token = request.headers['x_access_token']

        if not token:
            return common.rerror("로그인을 해주세요.", 403)

        common.cursor.execute("DELETE FROM sessions WHERE accessToken=%s", token)
        common.db.commit()
        return Response(status=204)

    except Exception as e:
        return common.rerror(e)


# refresh login token
@auth.route('/refresh', methods=['GET'])
def refresh_token():
    pass


# token to uuid
# TODO : check client ip and compare with common.db
# TODO : change token format to more random string
def token2uuid(token: str) -> str:
    common.cursor.execute("SELECT * from sessions where accessToken=%s", token)
    fetchs = common.cursor.fetchall()

    if not fetchs or len(fetchs) == 0:
        raise ValueError("Invalid Token")

    uuid = fetchs[0]['uuid']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    common.cursor.execute("UPDATE 'sessions' SET expiredate=%s WHERE accessToken=%s", (expiredate, token))
    common.db.commit()
    return uuid


