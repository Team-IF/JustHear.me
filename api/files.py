import hashlib
import os
import random
import shutil

from flask import Blueprint, request, send_from_directory, safe_join

from api import common

# upload files and download files

files = Blueprint('files', __name__)

root_storage = os.path.expanduser('~/files')
temp_storage = os.path.expanduser('~/files/temp')
serv_storage = 'files'

if not os.path.isdir(root_storage):
    os.mkdir(root_storage)
if not os.path.isdir(temp_storage):
    os.mkdir(temp_storage)


@files.route('/<hash_path>', methods=['POST'])
def upload(hash_path: str):
    try:
        file_path = safe_join(root_storage, hash_path)

        if not os.path.exists(file_path):
            file = request.files['file']

            temp_path = safe_join(temp_storage, str(random.randint(10000, 99999)))
            file.save(temp_path)

            hash_path = hashlib.sha1(file).hexdigest()
            file_path = safe_join(root_storage + '/' + hash_path)

            shutil.move(temp_path, file_path)

        url = ""
        if common.SSL:
            url += "https://"
        else:
            url += "http://"

        url += safe_join(request.headers['host'], serv_storage, hash_path)
        return url

    except KeyError as e:
        return common.rerror(e, 400)

    except Exception as e:
        return common.rerror(e, 500)


@files.route('/<hash_str>', methods=['GET'])
def download(hash_str: str):
    path = safe_join(root_storage, hash_str)
    if os.path.exists(path):
        return send_from_directory(root_storage, hash_str)
    else:
        return common.rerror("No such file", 404)
