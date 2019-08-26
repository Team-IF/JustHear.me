from flask import Blueprint, request, send_from_directory, safe_join
import random
import hashlib
import shutil
import os
from api import common

# upload files and download files

files = Blueprint('files', __name__)

root_storage = os.path.abspath('~/files')
temp_storage = os.path.abspath('~/files/temp')
serv_storage = 'files'


@files.route('/uploads', methods=['POST'])
def upload():
    try:
        file = request.files['file']

        temp_path = safe_join(temp_storage, random.randint(10000, 99999))
        file.save(temp_path)

        hash = hashlib.sha1(file).hexdigest()
        file_path = safe_join(root_storage + '/' + hash)

        shutil.move(temp_path, file_path)

        url = ""
        if app.SSL:
            url += "https://"
        else:
            url += "http://"

        url += safe_join(request.headers['host'], serv_storage, hash)
        return url

    except KeyError as e:
        return common.rerror(e, 400)

    except Exception as e:
        return common.rerror(e, 500)


@files.route('/uploads/<hash>', methods=['GET'])
def download(hash):
    return send_from_directory(root_storage, hash)
