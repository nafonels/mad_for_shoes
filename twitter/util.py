# !/usr/bin/env python
# -*- coding: utf-8 -*-


def extract_fields(tweet, fields: dict, append_from = {}):
    ret = append_from
    for key, json_key, default_type in ((x, *y) for x, y in fields.items()):
        ret[key] = extract_field(tweet, json_key, default_type)

    return ret


def extract_field(tweet, json_key, default_type):
    json_value = tweet
    for json_subkey in json_key.split(':'):
        json_value = json_value.get(json_subkey, default_type())
        if not json_value: break

    return json_value
