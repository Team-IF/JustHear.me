import hashlib
import os
import random
import shutil

from flask import Blueprint, request, send_from_directory, safe_join
from werkzeug.datastructures import FileStorage

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


@files.route('/<filename>', methods=['POST'])
def upload(filename: str):
    return upload_file(filename, request.files['file'])

def upload_file(filename: str, file: FileStorage):
    try:
        temp_path = safe_join(temp_storage, filename)
        file.save(temp_path)

        # TODO : 파일 이름을 해쉬로
        #hash_path = hashlib.sha1(file).hexdigest()

        hash_path = filename
        file_path = safe_join(root_storage, hash_path)

        handle_file(temp_path, file_path)

        url = common.protocol() + safe_join(request.headers['host'], serv_storage, hash_path)
        return url

    except KeyError as e:
        return common.rerror(e, 400)

    except Exception as e:
        return common.rerror(e, 500)

def handle_file(orginal_path, result_path):
    filename, ext = os.path.splitext(orginal_path)

    if ext == ".mp3":
        # original_path 의 파일을 어케어케 해서 result_path 에 저장시키면됨
        pass
    elif ext == ".aac":
        pass
    else:
        shutil.move(orginal_path, result_path)


@files.route('/<hash_str>', methods=['GET'])
def download(hash_str: str):
    path = safe_join(root_storage, hash_str)
    if os.path.exists(path):
        return send_from_directory(root_storage, hash_str)
    else:
        return common.rerror("No such file", 404)
