#!/usr/bin/env python3.8
# -- coding: utf-8 --

print("importing modules...")

from flask import Flask

from JsonResponse import JsonResponse
from api import *

print("Initializing Flask...")

app = Flask(__name__)
app.debug = True  # ONLY TO DEBUG #
app.response_class = JsonResponse
context = ('/etc/letsencrypt/live/teamif.io/fullchain.pem', "/etc/letsencrypt/live/teamif.io/privkey.pem")
common.SSL = True

app.register_blueprint(auth.auth, url_prefix='/auth')
app.register_blueprint(files.files, url_prefix='/files')
app.register_blueprint(profile.profile, url_prefix='/profile')
app.register_blueprint(test.test, url_prefix='/test')
app.register_blueprint(hear.hear, url_prefix='/hear')

print("Starting Server...")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, ssl_context=context, use_reloader=False)
#    app.run(host="0.0.0.0",port=7000)
