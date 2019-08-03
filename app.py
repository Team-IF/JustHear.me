from flask import Flask
import pymysql
import uuid

app = Flask(__name__)
db = "나도 몰라 이새끼야"
cursor = db.cursor()


@app.route('/', methods=['get'])
def hello_world():
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    return f'데이터베이스 버전은 {data}입니다. 생성된 uuid 는 {uuid.uuid4()}입니다'


if __name__ == '__main__':
    app.run()
