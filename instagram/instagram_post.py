#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse

from instagram.instagram_client import get_instagram_data
from util.data import extract_field, extract_fields
from util.logger import logger


def get_post_page(shortcode):
    node_path = 'p/'
    field = {
        '__a': 1,
    }
    logger.info(f'get {shortcode} post')
    return get_instagram_data(node_path, shortcode, field)


def get_custom_comment(post):
    post_head = 'graphql:shortcode_media'
    node = extract_field(post, post_head, dict)

    list_comments = extract_field(node, 'edge_media_to_comment:edges', list)
    if not len(list_comments):
        return None

    rets = []

    extract_spec = {
        'post_id':      ('id', str),
        'comment_text': ('created_at', int),
        'comment_date': ('text', str)
    }

    for comment in (x['node'] for x in list_comments):
        custom_comment = extract_fields(comment, extract_spec)

        custom_comment['post_id'] = 'insta_' + custom_comment['post_id']
        custom_comment['metadata'] = comment
        rets.append(custom_comment)

    return rets


def get_custom_post(post: dict) -> dict:
    post_head = 'graphql:shortcode_media'
    node = extract_field(post, post_head, dict)

    extract_spec = {
        'post_id':       ('id', str),
        'post':          ('edge_media_to_caption:edges', dict),
        'like_count':    ('edge_media_preview_like:count', int),
        'post_date':     ('taken_at_timestamp', int),
        'comment_count': ('edge_media_to_comment:count', int),
    }

    custom_post = extract_fields(node, extract_spec)

    # post 연결
    if isinstance(custom_post['post'], list):
        custom_post['post'] = '\n---\n'.join(x['node']['text'] for x in custom_post['post'])
    # post에서 hashtag 추출
    custom_post['hash_tag'] = (lambda s: s[s.find('#'):].replace('\n', ''))(custom_post['post'])
    custom_post['url'] = "https://www.instagram.com/p/%s/" % extract_field(node, 'shortcode', str)
    custom_post['post_id'] = 'insta_' + custom_post['post_id']
    custom_post['metadata'] = node

    return custom_post


def get_custom_media(post):
    post_head = 'graphql:shortcode_media'
    node = extract_field(post, post_head, dict)
    post_id = extract_field(node, 'id', str)
    list_media = extract_field(node, 'edge_sidecar_to_children:edges', list)

    # 무조건 이미지 하나는 포함됨
    list_media.append({'node': node})

    rets = []

    extract_spec = {
        'video_url': ('video_url', str),
    }

    for media in (x['node'] for x in list_media):
        custom_media = extract_fields(media, extract_spec)
        custom_media['file_url'] = media['display_resources'][-1]['src']
        custom_media['post_id'] = 'insta_' + post_id
        custom_media['file_path'] = parse.urlsplit(custom_media['file_url']).path.split(r'/')[-1]
        custom_media['file_path'] = (lambda s: r'/'.join([s[:4], s[4:]]))(custom_media['file_path'])
        custom_media['metadata'] = media
        rets.append(custom_media)

    return rets
