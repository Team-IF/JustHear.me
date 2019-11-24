#언제 완성할까
import bcrypt
from uuid import uuid4

'''
uuid = str(uuid4())
username = input()
email = input()
password = bcrypt.hashpw(input().encode('utf-8'), bcrypt.gensalt(10))
phonenumber = input()
gender = input()
profileImg = input()
profileMusic = input()
'''

uuid = str(uuid4())
username = 'PotatoY'
email = 'yjw_0412@naver.com'
pwd = '1234'.encode('utf-8')
password = bcrypt.hashpw(pwd, bcrypt.gensalt(10))
phonenumber = '+821011112222'
gender = 'M'
profileImg = ''
profileMusic = ''
