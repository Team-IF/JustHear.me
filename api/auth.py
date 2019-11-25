from flask import Blueprint, request, Response
import json
import bcrypt
import datetime
from uuid import uuid4
import JsonResponse
from api import common

# authicate user

auth = Blueprint('auth', __name__)

# LOGIN
# TODO : check email and pw validation
@auth.route('/login', methods=['post'])
def login():
    try:
        if not request.is_json:
            return app.rerror("invalid json", 400)

        req = request.json
        if not req.get('email') or not req.get("pw"):
            return app.rerror("이메일과 비밀번호를 입력해 주세요.", 400)

        app.cursor.execute("SELECT * from user_data where email=%s", request.json.get('email'))
        fetchs = app.cursor.fetchall()

        if not fetchs or len(fetchs) == 0:
            return app.rerror("잘못된 이메일/비밀번호", 403)

        data = fetchs[0]
        if bcrypt.checkpw(request.json.get('pass').encode('utf-8'), data.get('pass').encode('utf-8')):
            newtoken = str(uuid4())
            expiredate = datetime.datetime.utcnow()
            expiredate = expiredate + datetime.timedelta(days=14)
            app.cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ", (data['uuid'], newtoken, expiredate))
            app.db.commit()
            return JsonResponse(json.dumps({
                'token': newtoken,
                'uuid': data['uuid']
            }))
        else:
            return app.rerror("잘못된 이메일/비밀번호", 403)

    except Exception as e:
        return app.rerror(e, 500)

@auth.route('/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return app.rerror("invalid json", 400)
        
        req = request.json
    except Exception as e:
        return app.rerror(e, 500)

# delete login token
@auth.route('/login', methods=['DELETE'])
def invalidate_token():
    try:
        token = request.headers['x_access_token']

        if not token:
            return app.rerror("로그인을 해주세요.", 403)

        app.cursor.execute("DELETE FROM sessions WHERE accessToken=%s", token)
        app.db.commit()
        return Response(status=204)

    except Exception as e:
        return app.rerror(e)


# refresh login token
@auth.route('/refresh', methods=['GET'])
def refresh_token():
    pass


# token to uuid
# TODO : check client ip and compare with db
# TODO : change token format to more random string
def token2uuid(token: str) -> str:
    app.cursor.execute("SELECT * from sessions where accessToken=%s", token)
    fetchs = app.cursor.fetchall()

    if not fetchs or len(fetchs) == 0:
        raise ValueError("Invalid Token")

    uuid = fetchs[0]['uuid']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    app.cursor.execute("UPDATE 'sessions' SET expiredate=%s WHERE accessToken=%s", (expiredate, token))
    app.db.commit()
    return uuid


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")
