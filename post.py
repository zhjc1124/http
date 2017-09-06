import requests
post_url = 'http://123.206.16.144'
data = {'username': 'qwerty', 'password': 'zxcvbn'}


img = {'file': open('test.jpg', 'rb')}
response = requests.post(post_url, data=data, files=img)


print(response.text)
