import datetime
from uuid import uuid4

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

        user = common.User.fromEmail(req.get('email'))
        if not user or user.matchpw(req.get("pass")):
            return common.rerror("잘못된 이메일/비밀번호", 403)

        newtoken = str(uuid4())
        expiredate = datetime.datetime.utcnow()
        expiredate = expiredate + datetime.timedelta(days=14)
        common.cursor.execute("INSERT INTO sessions (uuid, accessToken, expiredate) VALUES (%s,%s,%s) ",
                              (data['uuid'], newtoken, expiredate))
        common.olddb.commit()
        return JsonResponse({
            'token': newtoken,
            'uuid': data['uuid']
        })

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

        uuids = (x['_id'] for x in common.db.user_data.find())
        print(uuids)
        uuid = str(uuid4())
        while uuid in uuids:
            uuid = str(uuid4())

        birth = req.get('birthday')
        if not birth:
            birth = None
        else:
            birth = datetime.datetime.strptime(birth, '%Y-%m-%d').date()

        values = (uuid,
                  req.get('username'),
                  req.get('email'),
                  req.get('pass'),
                  req.get('phonenumber'),
                  birth,
                  req.get('gender'),
                  req.get('profileImg'),
                  req.get('profileMusic'))
        user = common.User(*values)

        common.db.user_data.insert_one(user.toDict())
        return Response(status=204)

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
        common.olddb.commit()
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
    common.olddb.commit()
    return uuid
