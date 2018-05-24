# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib import parse

from util.logger import logger

base = "https://api.twitter.com/1.1/"


def get_twitter_data(client, node: str, field: dict):
    for k, v in dict(field).items():
        if not v:
            field.pop(k)

    encoded_field = parse.urlencode(field)
    url = base + node + '?' + encoded_field

    logger.info(f'request to "{url}"')
    logger.debug(f'request info : <base : "{base}"> <node: {node}> <encoded_field: {field}>')

    response, data = client.request(url)  # type : dict, bytes
    logger.debug(f'response status : {response["status"]}')

    try:
        if response['status'] == '200':
            ret = json.loads(data.decode('utf-8'))
            # print(ret)
            return ret
    except Exception as e:
        print("ERR:", e)
        logger.error('cannot responsed from : "%s" ' % (response['status'], url))
        logger.error('error message :', e)
        return None
