#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from setting import data_path


def save_json(platform: str, query: str, category: str, data: dict,
              page_id = None, page = None, is_raw = False):
    names = [
        query,
        platform,
        category,
    ]
    if page_id:
        names.append(str(page_id))
    if page:
        names.append(str(page))

    filename = '_'.join(names)
    filename = '/'.join([data_path,
                         'raw' if is_raw else '',
                         filename])

    with open(filename + '.json', 'w', encoding = 'utf-8') as outfile:
        str_ = json.dumps(data,
                          indent = 2,
                          ensure_ascii = False)
        outfile.write(str_)
