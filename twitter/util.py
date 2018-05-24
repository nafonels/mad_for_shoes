# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Teoslard'
__version__ = "$Revision$"


def extract_fields(tweet, fields: dict, append_from=None):
    ret = {} if not append_from else append_from
    for key, json_key, default_type in ((x, *y) for x, y in fields.items()):
        ret[key] = extract_field(tweet, json_key, default_type)

    return ret


def extract_field(tweet, json_key, default_type):
    json_value = tweet
    for json_subkey in json_key.split(':'):
        json_value = json_value.get(json_subkey, default_type())
        if not json_value: break

    return json_value


def add_list(to: list, data):
    if data:
        if isinstance(data, list):
            to.extend(data)
        else:
            to.append(data)