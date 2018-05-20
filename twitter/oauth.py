#!/usr/bin/env python
# -*- coding: utf-8 -*-
import oauth2


def oauth2_request(consumer_key, consumer_secret,
                   access_token, access_secret):
    try:
        consumer = oauth2.Consumer(key = consumer_key,
                                   secret = consumer_secret)
        token = oauth2.Token(key = access_token,
                             secret = access_secret)
        client = oauth2.Client(consumer, token)
        return client

    except Exception as e:
        print(e)
        return None
