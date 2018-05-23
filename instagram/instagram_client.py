# !/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import count
from urllib import parse

import requests

from util.logger import logger

base = 'https://www.instagram.com/'


def get_instagram_data(node_path: str, keyword: str, field: dict):
    for k, v in field.items():
        if not v:
            field.pop(k)

    field = parse.urlencode(field)
    url = base + node_path + keyword + '/?' + field

    try_count = count(0)
    next(try_count)
    while 1:
        logger.info(f'request to "{url}"')
        logger.debug(f'request info : <base : "{base}"> <node_path: {node_path}>'
                     f' <keyword: {keyword}> <encoded_field: {field}>')
        response = requests.get(url)
        logger.debug(f'response status : {response.status_code}')

        try:
            if response.status_code == 200:
                ret = response.json()
                return ret

            else:
                logger.warn('connection error : %s' % response.status_code)
                if next(try_count) > 3:
                    logger.error(f'cannot connect to "{url}"')
                    return None


        except Exception as e:
            print("ERR:", e)
            logger.error('cannot responsed from : "%s" ' % (response.status_code, url))
            logger.error('error message :', e)
            return None

        next(try_count)
