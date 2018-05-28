#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from itertools import count

from instagram.instagram_client import get_instagram_data
from instagram.instagram_post import get_post_page, get_custom_comment, get_custom_post, get_custom_media
from util.data import add_list
from util.iofunc import save_json
from util.logger import logger


def search_query(query, next_cursor = None, date_to = '2018/05/01'):
    c = count(1)
    is_break = False
    is_date_break = False
    is_final = False

    next_cursor = next_cursor

    while 1:
        try:
            i = next(c)
            logger.info(f'get posts <page {i:04d} - next_cursor : {next_cursor}> : {query}')

            json_post = []
            json_comments = []
            json_media = []

            # get json w/t endpoint
            results = get_search_list(query, next_cursor)

            if not next_cursor:
                next_cursor = 'first'
            # next_endpoint 획득

            edge_hashtag = results['graphql']['hashtag']['edge_hashtag_to_media']
            page_info = edge_hashtag['page_info']


            save_json('insta', query, 'list', results, i, next_cursor, True)

            page_edges = edge_hashtag['edges']

            for node in (x['node'] for x in page_edges):
                timestamp = node['taken_at_timestamp']
                if timestamp < datetime.strptime(date_to, '%Y/%m/%d').timestamp():
                    logger.info('we crawled enough data')
                    is_break = True
                    is_date_break = True
                data = get_post(node['shortcode'])
                add_list(json_post, data[0])
                add_list(json_comments, data[1])
                add_list(json_media, data[2])

        except KeyboardInterrupt:
            is_break = True

        except Exception as e:
            logger.error('cannot crawl tweet data.')
            logger.critical(f'you can try with next_cursor : {next_cursor}')
            print(e)
            break


        logger.info('save scrap data')

        save_json('insta', query, 'post', json_post, next_cursor, i)
        save_json('insta', query, 'comment', json_comments, next_cursor, i)
        save_json('insta', query, 'media', json_media, next_cursor, i)

        if page_info['has_next_page']:
            next_cursor = page_info['end_cursor']
        else:
            is_final = True

        if is_final:
            logger.info('final page_crawled')
            next_cursor = None
            break

        if is_break:
            logger.debug('loop break')
            break

    if is_date_break:
        logger.debug('enough data crawled. <date : %s ~ >' % date_to)

    logger.info('search "{}" SAVED'.format(query))

    if next_cursor == 'first':
        next_cursor = None
    return next_cursor


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
    search_query(keyword)
