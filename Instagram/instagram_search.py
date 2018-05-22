#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib import parse

import requests

init_url = 'https://www.instagram.com/explore/tags/%s/?__a=1' % (keyword)


def search(keyword):
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
    next_resp = get_search_list(keyword, next_cursor)
    next_resp
    # json 데이터 출력
    resp_json = next_resp.json()
    # print(resp_json)
    # for문으로 원하는 수만큼 json 파일 생성
    i = count(1)
    while 1:
        # next_endpoint 획득
        paging = resp_json['graphql']['hashtag']['edge_hashtag_to_media'][
            'page_info']
        if paging['has_next_page']:
            next_cursor = paging['end_cursor']
        next_cursor

        # 얻은 endpoint로 접속
        next_resp = get_search_list(keyword, next_cursor)
        next_resp

        # json 데이터 출력
        resp_json = next_resp.json()
        print(resp_json)
        with open('shoes_instagram%s.json' % (i), 'w', encoding = 'utf-8') as outfile:
            insta = json.dumps(resp_json, ensure_ascii = False)
            outfile.write(insta)
        i = i + 1

        if i > 10: break


def get_search_list(keyword, next_cursor):
    node_path = 'explore/tags/'
    field = {
        '__a':    1,
        'max_id': next_cursor
    }

    next_resp = get_instagram_data(node_path, keyword, field)
    return next_resp


def get_instagram_data(node_path, keyword, field):
    base = 'https://www.instagram.com/'
    field = parse.urlencode(field)
    url = base + node_path + keyword + '?' + field

    response = requests.get(url)
    try:
        if response.status_code == '200':
            ret = response.json()
            return ret
    except Exception as e:
        print("ERR:", e)
        return None


if __name__ == '__main__':
    keyword = '신발'
    search(keyword)
