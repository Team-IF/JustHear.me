# -- coding: utf-8 --
from __future__ import annotations

import datetime
import enum
import json
import re
import secrets
import traceback
import typing
import uuid
from typing import Union, List

import bcrypt
import pymongo
import pymysql

import JsonResponse

SSL = True
emailregex = re.compile('^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$')


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


class Gender(enum.Enum):
    M = 'M'
    F = 'F'


class User:
    def __init__(self, uid: typing.Union[str, uuid.UUID], username: str, email: str, password: str,
                 birthday: datetime.date = None,
                 gender: Gender = None, profileimg=None, profilemusic=None):
        if isinstance(uid, str):
            self.uuid: uuid.UUID = uuid.UUID(uid)
        elif isinstance(uid, uuid.UUID):
            self.uuid: uuid.UUID = uid
        else:
            raise TypeError("uid have to be type 'uuid.UUID' or 'str'")
        self.username: str = username
        if emailregex.match(email):
            self.email = email
        else:
            raise ValueError("Invaild E-mail format")
        self.password = hashpw(password)
        self.birthday: datetime.date = birthday
        self.gender: Gender = gender
        self.profileImg = profileimg
        self.profileMusic = profilemusic

    @property
    def __dict__(self):
        return {'uuid': self.uuid, 'username': self.username, 'email': self.email, 'birthday': self.birthday,
                'gender': self.gender, 'profileImg': self.profileImg, 'profileMusic': self.profileMusic}

    def matchpw(self, passwd):
        return bcrypt.checkpw(passwd.encode('utf-8'), self.password.encode('utf-8'))


class Hear:
    def __init__(self, title: str, content: str, author: User):
        self.id: str = secrets.token_urlsafe(10)
        self.title: str = title
        self.content: str = content
        self.author: User = author
        self.comments: List[Hear] = []

    @property
    def __dict__(self):
        return {'id': self.id, 'title': self.title, 'content': self.content, 'author': self.author}

    def addcomment(self, comment: Hear):
        self.comments.append(comment)


def rerror(ex: Union[Exception, str], status_code: int = 400) -> JsonResponse.JsonResponse:  # response error
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

conn = pymongo.MongoClient('mongodb://%s:%s@localhost' % ('hearme', 'dhdh4321'))
db = conn.hearme

olddb = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                        charset="utf8")

cursor = olddb.cursor(pymysql.cursors.DictCursor)
