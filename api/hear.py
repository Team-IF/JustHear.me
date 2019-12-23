import datetime
from uuid import uuid4

from flask import Blueprint, request, Response, safe_join
from werkzeug.datastructures import ImmutableMultiDict

from api import common, files

from .common import (
    Hear,
    User
)

# authenticate user

hear = Blueprint('hear', __name__)

@hear.route('/upload', methods=['POST'])
def upload():
    try:
        data = dict(request.form)

        content = list()
        author = data.get("author")
        content = data.get("content")

        files_info = data.get("fileinfo") # 파일목록
        files_url = list()

        if files_info:
            for name in files_info.split(";"):
                file_value = request.files.get(name)

                if file_value:
                    u = files.upload_file(file_value.filename, file_value)
                    files_url.append(u)

        # 글 정보
        HEAR_DATA = (author, content, files_url)

        # debug
        return data
    
    except Exception as e:
        raise e
        return common.rerror(e, 500)


@hear.route('/test', methods=['GET'])
def test():
    return Response("""
    <html><head></head><body>
    <form action="/hear/upload" method="POST" enctype="multipart/form-data">
        Author : <br>
        <input type="text" name="author">
        Content : <br>
        <input type="text" name="content">
        Your file : <br>
        <input type="file" name="file1">

        <input type="hidden" name="fileinfo" value="file1;">
        <br>
        <input type="submit">
    </form>
    </body></html>
    """, mimetype="text/html")
