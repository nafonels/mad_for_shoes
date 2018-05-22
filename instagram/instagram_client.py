# !/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse

import requests

base = 'https://www.instagram.com/'


def get_instagram_data(node_path: str, keyword: str, field: dict):
    field = parse.urlencode(field)
    url = base + node_path + keyword + '?' + field

    response = requests.get(url)
    print(response.text)
    print(response.status_code)
    try:
        if response.status_code == 200:
            ret = response.json()
            return ret

    except Exception as e:
        print("ERR:", e)
        return None
