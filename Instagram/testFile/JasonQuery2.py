import json

import requests
from urllib import parse as p

h = {'Referer': 'https://www.instagram.com/explore/tags/%EC%8B%A0%EB%B0%9C/',
     'Cookie': 'rur=ATN; csrftoken=pL3KuLyMPY1Q353XikQy6WzXhlysbsZo; mid=WvlIuwA'
               'LAAHZqXOhGLxAC-rOgGJQ; urlgen="{\"time\": 1526286523\054 \"61.74.'
               '225.2\": 4766}:1fI98I:3L0Midub3tCxBwVVqwBP6VFUDI8',
     'X-Instagram-GIS': 'e311f7db8a7e0c0f7a37d53a5b86bb4d',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                   ' (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
     }

url = 'https://www.instagram.com/graphql/query/?' + '&'.join(
    ['query_hash=ded47faa9a1aaded10161a2ff32abb6b', 'variables='])

quote_before = '%7B%22tag_name%22%3A%22%EC%8B%A0%EB%B0%9C%22%2C%22first%22%3A2%' \
               '2C%22after%22%3A%22AQAUKt5tsa-bcgWwyQI68wSiFmeYXlhY17NQbMafBM-8r4' \
               'eiacm2XMWJLqtick3awpWevu4GbdULvlrZSdvTkBPNNKe9HrPFzJmYRgc1KhmIvA%22%7D'

unqu = p.unquote(quote_before)
a = '{"tag_name":"신발","first":10,"after":"AQBWkrdH3CXPCIrHUbQfpqm8cQDob7o7PNO0g' \
    'ZzEzslDutg948BgvnJO_aJNu5xd0RxZzgi_58lV2DdRsS6ymq4PksWMRwsodxvGOvZQxfq35w"}'
b = '{"tag_name":"신발","first":10,"after":"AQBWkrdH3CXPCIrHUbQfpqm8cQDob7o7PNO0g' \
    'ZzEzslDutg948BgvnJO_aJNu5xd0RxZzgi_58lV2DdRsS6ymq4PksWMRwsodxvGOvZQxfq35w"}'
quote_after = p.quote(b)

url = url + quote_after

resp1 = requests.get(url, headers=h)
print(resp1)
# print(dir(resp1))
# print(resp1.json())
j = resp1.json()
print(j)
with open('shoes_instagram.json', 'w', encoding='utf-8') as outfile:
    insta = json.dumps(j, ensure_ascii=False)
    outfile.write(insta)
