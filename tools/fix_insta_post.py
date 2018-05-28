#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from glob import glob

from setting import data_path

search_pattern = '*insta_post_*.json'

file_list = glob(data_path + search_pattern)

for file_path in file_list:
    with open(file_path, 'r', encoding = 'utf-8') as rp:
        data = json.load(rp)

    for iter in data:
        # print(iter['post'])
        # if not iter['post']:
        post_edge = iter['metadata']['edge_media_to_caption']['edges']
        # print(post_edge)
        # post_edeg =
        iter['post'] = '\n---\n'.join(x['node']['text'] for x in post_edge)
        # a = ' '.join(
        iter['hash_tag'] = ' '.join(
                (lambda s: s[s.find('#'):].replace('\n', ' '))
                (x['node']['text']) for x in post_edge)

    # print(data)

    with open(file_path, 'w', encoding = 'utf-8') as fp:
        json.dump(data, fp,
                  indent = 2,
                  ensure_ascii = False)

        print('fixed:', file_path)
