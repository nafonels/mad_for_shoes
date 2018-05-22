#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import count

from instagram.instagram_client import get_instagram_data
from instagram.instagram_post import get_post_page, get_custom_comment, get_custom_post, get_custom_media
from util.data import add_list
from util.iofunc import save_json


def search(query, page_break = 10):
    next_cursor = None
    c = count(1)

    while 1:
        i = next(c)
        print(i)
        json_post = []
        json_comments = []
        json_media = []

        # get json w/t endpoint
        results = get_search_list(query, next_cursor)
        if i > page_break: break

        # next_endpoint 획득

        edge_hashtag = results['graphql']['hashtag']['edge_hashtag_to_media']
        page_info = edge_hashtag['page_info']
        if page_info['has_next_page']:
            next_cursor = page_info['end_cursor']

        # print json
        # print(results)

        save_json('insta', query, 'list', results, i, True)

        page_edges = edge_hashtag['edges']
        # print(page_edges)
        # get_post_shortcode
        for node in (x['node'] for x in page_edges):
            data = get_post(node['shortcode'])
            add_list(json_post, data[0])
            add_list(json_comments, data[1])
            add_list(json_media, data[2])

        # print(json_post)
        # print(json_comments)
        # print(json_media)
        save_json('insta', query, 'post', json_post, i)
        save_json('insta', query, 'comment', json_comments, i)
        save_json('insta', query, 'media', json_media, i)

    print(f'{query} SAVED')


def get_post(shortcode):
    post = get_post_page(shortcode)
    _p = get_custom_post(post)
    _c = get_custom_comment(post)
    _m = get_custom_media(post)

    return _p, _c, _m


def get_search_list(keyword, next_cursor = None):
    node_path = 'explore/tags/'
    field = {
        '__a': 1,
    }
    if next_cursor:
        field['max_id'] = next_cursor

    return get_instagram_data(node_path, keyword, field)


if __name__ == '__main__':
    keyword = '신발'
    search(keyword)
