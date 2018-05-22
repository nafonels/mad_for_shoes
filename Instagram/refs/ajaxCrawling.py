# Json load가 안됨

import sys
import requests
import json

import urllib.request

import json
import simplejson

import datetime

import requests
URL = 'https://www.instagram.com/static/bundles/base/TagPageContainer.js/8551280fb8d9.js' # queryId가 있는 JS파일 URL
response = requests.get(URL)
response.status_code
print(response.text)

j = response.text
print(j['id'])




# url = 'https://www.instagram.com/static/bundles/base/TagPageContainer.js/8551280fb8d9.js'

# url = "https://www.instagram.com/static/bundles/base/TagPageContainer.js/8551280fb8d9.js"+"?format=json"
# data = requests.get(url)
# print(data)
# json_data = json.load()
# u = urllib.request.urlopen(url)
#
# data = u.read()
#
# print(data)

# response = urllib.request.urlopen(url)
# data = json.load(response.decode('UTF-8'))

# response = urllib.request.urlopen(url)
# data = json.load(response)

# data = str(data).strip("'<>() ").replace('\'', '\"')
# data = data.replace('\0', '')
# print(data)
# j = simplejson.load(data)
#
# info = json.loads(data.decode("utf-8"))







# json header에 있는 json url 주소
# json_url = 'https://www.instagram.com/static/bundles/base/TagPageContainer.js/8551280fb8d9.js'
# headers = {'Referer': 'https://www.instagram.com/explore/tags/%EC%8B%A0%EB%B0%9C/',
#            'Cookie': 'rur=ATN; csrftoken=pL3KuLyMPY1Q353XikQy6WzXhlysbsZo; mid=WvlIuwALAAHZqXOhGLxAC-rOgGJQ; urlgen="{&quot;time&quot;: 1526286523\054 &quot;61.74.225.2&quot;: 4766}:1fI98I:3L0Midub3tCxBwVVqwBP6VFUDI8',
#            'X-Instagram-GIS': 'e311f7db8a7e0c0f7a37d53a5b86bb4d',
#            'User-Agent' : ''
#            }
# 받아온 json을 텍스트로 변환
# json_string = requests.get(json_url)



# print(json_string)
# # json모듈을 사용해서 로드
# data_list = json.loads(json_string)

# print(data_list)



