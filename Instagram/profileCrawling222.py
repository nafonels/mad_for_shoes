import json, re, requests
import urllib.request
from bs4 import BeautifulSoup

# [ user_id 입력 ]
user = 'comeonyeol'
profile = 'https://www.instagram.com/' + user

# [ 무한루프를 위한 end_cursor 따오기와 window_sharedData 저장 ]

# [ BeautifulSoup로 시도 ]
html = urllib.request.urlopen(profile)
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
body = soup.find('body')
tags = body.findAll('script', attrs={'type': 'text/javascript'})
# print(len(tags))
# print(tags[0].text) # window._sharedData는 첫번째
# print(tags[0].text[21:-1]) # json에 필요한 글자만 출력
data = tags[0].text[21:-1]
j = json.loads(data)
print(j)

# [ 정규표현식으로 시도 ]
with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'
    end_cursor = ''
    for count in range(1, 3):
        print('PAGE: ', count)
        r = s.get(profile, params={'max_id': end_cursor})
        data = re.search(
            r'window._sharedData = (\{.+?});</script>', r.text).group(1)
        j = json.loads(data)
        # [ 필요 데이터만 추출 ]
        print(j)
        media = j['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

        for node in (x['node'] for x in media['edges']):
            if node['is_video']:
                page = 'https://www.instagram.com/p/' + node['shortcode']
                r = s.get(page)
                url = re.search(r'"display_url": ?"([^"]+)"', r.text).group(1)
                print('VIDEO:', url)
            else:
                print('TEXT:', node['edge_media_to_caption'])

        end_cursor = re.search(r'"end_cursor": ?"([^"]+)"', r.text).group(1)
