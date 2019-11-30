#!/usr/bin/env python3.8
# -- coding: utf-8 --

print("import modules")

import pymysql
from flask import Flask

from JsonResponse import JsonResponse
from api import *

print("Initialize Flask")

app = Flask(__name__)
app.debug = True  # ONLY TO DEBUG #
app.response_class = JsonResponse
context = ('/etc/letsencrypt/live/nanobot.tk/fullchain.pem', "/etc/letsencrypt/live/nanobot.tk/privkey.pem")
common.SSL = True

app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(files.files, url_prefix='/files')
app.register_blueprint(profile.profile, url_prefix='/profile')
app.register_blueprint(test.test, url_prefix='/test')

print("Start Server")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context, use_reloader=False)
#    app.run(host="0.0.0.0",port=7000)
