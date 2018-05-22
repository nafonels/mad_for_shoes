#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from itertools import count

import requests

from instagram.instagram_client import get_instagram_data


def search(query):
    next_cursor = None
    c = count(1)

    while 1:
        i = next(c)

        # get json w/t endpoint
        results = get_search_list(query, next_cursor)
        if i > 10: break

        # next_endpoint 획득
        page_info = results['graphql']['hashtag']['edge_hashtag_to_media']['page_info']
        if page_info['has_next_page']:
            next_cursor = page_info['end_cursor']
        next_cursor

        # print json
        print(results)

        with open('shoes_instagram%s.json' % (i), 'w', encoding = 'utf-8') as outfile:
            insta = json.dumps(results, ensure_ascii = False)
            outfile.write(insta)


def get_search_list(keyword, next_cursor = None):
    node_path = 'explore/tags/'
    field = {
        '__a':    1,
        'max_id': next_cursor
    }

    return get_instagram_data(node_path, keyword, field)


if __name__ == '__main__':
    keyword = '신발'
    search(keyword)
