from flask import Blueprint, request
import json
from api import common, auth

# manage users

profile = Blueprint('profile', __name__)


def get_profile(uuid: str):
    app.cursor.execute("SELECT * from user_data where uuid=%s", uuid)
    fetchs = app.cursor.fetchall()

    if not fetchs or len(fetchs) == 0:
        raise ValueError("해당 유저를 찾을 수 없습니다.")

    data = fetchs[0]
    data['birthday'] = data['birthday'].strftime('%Y-%m-%d')
    del data['uuid'], data['pass']
    return data


# GET someone's profile
@profile.route('/profile/<uuid>', methods=['get'])
def profile_get(uuid: str):
    try:
        p = get_profile(uuid)
        return json.dumps(p)

    except ValueError as e:  # can't find user
        return common.rerror(e, 404)

    except Exception as e:  # other error
        return common.rerror(e, 500)


# EDIT my profile (계정주인만 수정가능)
@profile.route('/profile/<uuid>', methods=['put'])
def profile_edit(uuid: str):
    try:
        if not request.is_json:
            return common.rerror("invalid json", 400)

        token = request.headers['x_access_token']

        if not token:
            return common.rerror("로그인을 해주세요.", 401)
        if uuid != auth.token2uuid(token):
            return common.rerror("자신의 프로필만 수정할 수 있습니다.", 403)

        args = request.json
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

    except Exception as e:
        return common.rerror(e, 500)

