# !/usr/bin/env python
# -*- coding: utf-8 -*-
from twitter.twitter_client import get_twitter_data


def get_user_timeline(client, screen_name, count = 50, include_rts = False):
    node = "statuses/user_timeline.json"
    field = {
        'screen_name': screen_name,
        'count':       count,
        'include_rts': include_rts,
    }

    return get_twitter_data(client, node, field)
