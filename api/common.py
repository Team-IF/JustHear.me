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
from typing import Union

import bcrypt
import pymongo
import pymysql

from JsonResponse import JsonResponse

SSL = True
emailregex = re.compile('^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$')
phoneregex = re.compile('[+][0-9]+')


def hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def protocol():
    if SSL:
        return "https://"
    else:
        return "http://"


class Gender(enum.Enum):
    M = 'M'
    F = 'F'


class User:
    def __init__(self, uid: typing.Union[str, uuid.UUID], username: str, email: str, password: str, phonenumber: str,
                 birthday: datetime.date,
                 gender: Gender, profileimg, profilemusic):

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

        if phoneregex.match(phonenumber):
            self.phonenumber = phonenumber
        else:
            raise ValueError("Invaild Phone Number format")

        self.password = hashpw(password)
        self.birthday: datetime.date = birthday
        self.gender: Gender = gender
        self.profileImg = profileimg
        self.profileMusic = profilemusic

    def toDict(self):
        d = self.__dict__
        d['_id'] = d.pop('uuid', None)
        return d

        # return {
        #    '_id': self.uuid,
        #    'username': self.username,
        #    'email': self.email,
        #    'password': self.password,
        #    'phonenumber': self.phonenumber,
        #    'birthday': self.birthday,
        #    'gender': self.gender,
        #    'profileImg': self.profileImg,
        #    'profileMusic': self.profileMusic
        # }

    def matchpw(self, passwd):
        return bcrypt.checkpw(passwd.encode('utf-8'), self.password.encode('utf-8'))

    @classmethod
    def fromUUID(cls, uid: Union[uuid.UUID, str]):
        if isinstance(uid, str):
            uid: uuid.UUID = uuid.UUID(uid)
        elif isinstance(uid, uuid.UUID):
            uid: uuid.UUID = uid
        result = db.user_data.find_one({"_id": uid})
        if not result:
            return None
        else:
            return cls(**result)

    @classmethod
    def fromEmail(cls, email: str):
        result = db.user_data.find_one({"email": email})
        if not result:
            return None
        else:
            return cls(**result)


class Hear:
    def __init__(self, title: str, content: str, author: User):
        self.id: str = secrets.token_urlsafe(10)
        self.title: str = title
        self.content: str = content
        self.author: User = author

    def toDict(self):
        return {
            '_id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author}


def rerror(ex: Union[Exception, str], status_code: int = 400) -> JsonResponse.JsonResponse:  # response error
    r = JsonResponse()
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

conn = pymongo.MongoClient('mongodb://%s:%s@localhost/%s' % ('hearme', 'dhdh4321', 'hearme'))
db = conn.hearme

olddb = pymysql.connect(unix_socket="/var/run/mysqld/mysqld.sock", user="hearme", password="dhdh4321", db="hearme",
                        charset="utf8")

cursor = olddb.cursor(pymysql.cursors.DictCursor)
