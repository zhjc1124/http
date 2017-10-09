# -*- coding: utf8-*-
import requests
from urllib import urlencode
post_url = 'http://123.206.16.144'
data = {'Username': 'qwerty', '\xac\xa6': '00000000', '\xcf\xa6': '120', '0@': u'测试'}
data = urlencode(data)
print type(data)
img = {'file': open('test.jpg', 'rb')}
response = requests.post(post_url, data=data, files=img)

print(response.text)
