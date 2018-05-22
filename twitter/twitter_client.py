# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib import parse

base = "https://api.twitter.com/1.1/"


def get_twitter_data(client, node: str, field: dict):
    field = parse.urlencode(field)
    url = base + node + '?' + field

    response, data = client.request(url)  # type : dict, bytes
    # print(data.decode('utf-8'))
    # data = data.decode('utf-8')
    # print(json.loads(data))

    try:
        if response['status'] == '200':
            ret = json.loads(data.decode('utf-8'))
            # print(ret)
            return ret
    except Exception as e:
        print("ERR:", e)
        return None
