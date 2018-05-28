#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from glob import glob
from urllib import parse

from setting import data_path
from util.data import extract_field, extract_fields

search_pattern = '*insta_post_*.json'

file_list = glob(data_path + search_pattern)

for file_path in file_list:
    with open(file_path, 'r', encoding = 'utf-8') as rp:
        data = json.loads(rp.read())
    json_media = []

    for node in (x for x in data):
        # print(extract_field(node, 'metadata:shortcode', str))
        # fix url
        node['url'] = "https://www.instagram.com/p/%s/" % extract_field(node, 'metadata:shortcode', str)
        # print(node['url'])

        meta = extract_field(node, 'metadata', dict)
        post_id = extract_field(meta, 'id', str)
        list_media = extract_field(meta, 'edge_sidecar_to_children:edges', list)

        # 무조건 이미지 하나는 포함됨
        list_media.append({'node': meta})

        rets = []

        extract_spec = {
            'video_url': ('video_url', str),
        }

        _dup_check = []
        for media in (x['node'] for x in list_media):
            custom_media = extract_fields(media, extract_spec)
            custom_media['file_url'] = media['display_resources'][-1]['src']
            if custom_media['file_url'] in _dup_check:
                continue
            custom_media['post_id'] = 'insta_' + post_id
            custom_media['file_path'] = parse.urlsplit(custom_media['file_url']).path.split(r'/')[-1]
            custom_media['file_path'] = (lambda s: r'/'.join([s[:4], s[4:]]))(custom_media['file_path'])
            custom_media['metadata'] = media
            rets.append(custom_media)

        json_media.extend(rets)

    # print(json_media)
    # print(file_path.split('_'))

    with open(file_path, 'w', encoding = 'utf-8') as fp:
        json.dump(data, fp,
                  indent = 2,
                  ensure_ascii = False)
    media_file = file_path.split('_')
    media_file[2] = 'media'
    media_file = '_'.join(media_file)
    print(media_file)
    with open(media_file, 'w', encoding = 'utf-8') as fp:
        json.dump(json_media, fp,
                  indent = 2,
                  ensure_ascii = False)
