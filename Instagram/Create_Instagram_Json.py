import json

import requests


# keyword 및 target url 설정
keyword = '신발'
init_url = 'https://www.instagram.com/explore/tags/%s/?__a=1' % (keyword)

# 접속
init_resp = requests.get(init_url)
init_resp

# json 데이터 출력
resp_json = init_resp.json()
# print(resp_json)

# next_endpoint 획득
paging = resp_json['graphql']['hashtag']['edge_hashtag_to_media']['page_info']
if paging['has_next_page']:
    next_cursor = paging['end_cursor']
next_cursor

# 얻은 endpoint로 접속
next_url = 'https://www.instagram.com/explore/tags/%s/?__a=1&max_id=%s' % (keyword, next_cursor)
next_resp = requests.get(next_url)
next_resp

# json 데이터 출력
resp_json = next_resp.json()
# print(resp_json)

# for문으로 원하는 수만큼 json 파일 생성
i = 0
while i <= 10 :
    # next_endpoint 획득
    paging = resp_json['graphql']['hashtag']['edge_hashtag_to_media'][
        'page_info']
    if paging['has_next_page']:
        next_cursor = paging['end_cursor']
    next_cursor

    # 얻은 endpoint로 접속
    next_url = 'https://www.instagram.com/explore/tags/%s/?__a=1&max_id=%s' % (
    keyword, next_cursor)
    next_resp = requests.get(next_url)
    next_resp

    # json 데이터 출력
    resp_json = next_resp.json()
    print(resp_json)
    with open('shoes_instagram%s.json'%(i), 'w', encoding='utf-8') as outfile:
        insta = json.dumps(resp_json, ensure_ascii=False)
        outfile.write(insta)
    i = i + 1