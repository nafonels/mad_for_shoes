import requests
import json

# json header에 있는 json url 주소
json_url = 'https://www.instagram.com/graphql/query/?query_hash=ded47faa9a1aaded10161a2ff32abb6b&variables=%7B%22tag_name%22%3A%22%EC%8B%A0%EB%B0%9C%22%2C%22first%22%3A10%2C%22after%22%3A%22AQC4u4KIPhhO0Xj3YDwl8GUbkjpQKG4tRTonYA5tF5J0X13UwnZ3XU532Wq8KufOPaS0OwIoDu2efMLtQaFsPTpCoCUO8IT9MiKhyrw38mTNzQ%22%7D'
headers = {'Referer': 'https://www.instagram.com/explore/tags/%EC%8B%A0%EB%B0%9C/',
           'Cookie': 'rur=ATN; csrftoken=pL3KuLyMPY1Q353XikQy6WzXhlysbsZo; mid=WvlIuwALAAHZqXOhGLxAC-rOgGJQ; urlgen="{&quot;time&quot;: 1526286523\054 &quot;61.74.225.2&quot;: 4766}:1fI98I:3L0Midub3tCxBwVVqwBP6VFUDI8',
           'X-Instagram-GIS': 'e311f7db8a7e0c0f7a37d53a5b86bb4d',
           }
# 받아온 json을 텍스트로 변환
json_string = requests.get(json_url)



print(json_string)
# # json모듈을 사용해서 로드
# data_list = json.loads(json_string)
#
# print(data_list)