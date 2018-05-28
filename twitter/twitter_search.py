import json
from itertools import count
from urllib import parse

from datetime import datetime, timedelta

from config import twitter_consumer_key, twitter_consumer_secret, \
    twitter_access_token, twitter_access_secret
from util.iofunc import save_json
from util.logger import logger
from setting import data_path
from twitter.oauth import oauth2_request
from twitter.twitter_client import get_twitter_data
from util.data import extract_fields, extract_field, add_list


def get_searched_tweet(client, search_query, count = 100, max_id = None):
    """

    :param client:
    :param search_query:
    :param count:
    :param max_id: int
    :return:
    """
    node = "search/tweets.json"
    field = {
        'q':      search_query,
        'count':  count,
        'max_id': max_id,
    }

    return get_twitter_data(client, node, field)


def get_rate_limit(client, resources: list):
    node = "application/rate_limit_status.json"
    field = {
        'resources': ','.join(resources),
    }

    return get_twitter_data(client, node, field)


# extract_tweet
def get_custom_post(tweet: dict) -> dict:
    extract_spec = {
        'post_id':       ('id_str', str),
        'post':          ('text', str),
        'hash_tag':      ('entities:hashtags', str),
        'like_count':    ('favorite_count', str),
        'post_date':     ('created_at', str),
        'comment_count': ('retweet_count', int),
        'extended':      ('extended_tweet', bool),
    }

    custom_tweet = extract_fields(tweet, extract_spec)
    custom_tweet['post_id'] = 'twi_' + custom_tweet['post_id']
    custom_tweet['url'] = 'https://twitter.com/{user_screenid}/status/{tweet_id}'. \
        format_map({'user_screenid': tweet['user']['screen_name'], 'tweet_id': tweet['id_str']})
    custom_tweet['extended'] = True if custom_tweet['extended'] else False
    custom_tweet['metadata'] = tweet
    return custom_tweet


def get_custom_comment(tweet: dict) -> dict:
    keys = tweet.keys()
    extract_spec = {
        'comment_text': ('text', str),
        'comment_date': ('created_at', str),
        'comment_id':   ('id_str', str)
    }
    custom_comment = {}

    if 'retweeted_status' in keys:  # retweet
        extract_spec['post_id'] = ('retweeted_status:id_str', str)
        custom_comment['type'] = 'retweet'
        extract_spec['metadata'] = ('retweeted_status', str)

    elif tweet.get('is_quote_status', False):  # quote
        extract_spec['post_id'] = ('quoted_status_id_str', str)
        custom_comment['type'] = 'quote'
        extract_spec['metadata'] = ('quoted_status', str)

    elif tweet.get('in_reply_to_status_id', False):  # reply
        extract_spec['post_id'] = ('in_reply_to_status_id_str', str)
        custom_comment['type'] = 'reply'
        custom_comment['metadata'] = ''
    else:
        custom_comment = None

    if custom_comment:
        custom_comment = extract_fields(tweet, extract_spec, custom_comment)
        custom_comment['post_id'] = 'twi_' + custom_comment['post_id']
        custom_comment['comment_id'] = 'twi_' + custom_comment['comment_id']

    return custom_comment


def get_custom_media(tweet: dict) -> dict:
    list_media = extract_field(tweet, 'extended_entities:media', list)
    post_id = 'twi_' + tweet['id_str']

    if not len(list_media):
        return None
    rets = []
    for media in list_media:
        extract_spec_media = {
            'file_url':  ('media_url', str),
            'video_url': ('video_info:variants', str),
        }

        custom_media = extract_fields(media, extract_spec_media)
        custom_media['post_id'] = post_id
        custom_media['video_url'] = custom_media['video_url'][-1]['url'] if custom_media['video_url'] else ''
        custom_media['file_path'] = parse.urlsplit(custom_media['file_url'])[2].split(r'/')[-1]
        custom_media['file_path'] = r'/'.join([custom_media['file_path'][:4], custom_media['file_path'][4:]])
        custom_media['metadata'] = media

        rets.append(custom_media)
    return rets


def search_query(query, num_posts = 100, next_id = None):
    client = oauth2_request(twitter_consumer_key, twitter_consumer_secret,
                            twitter_access_token, twitter_access_secret)

    # tweets = get_searched_tweet(client, query, num_posts)
    # print(type(tweets))
    # print(tweets)

    c = count(1)
    logger.debug('get api rate limit')
    limit_result = get_rate_limit(client, ['search'])
    api_limit = extract_field(limit_result, 'resources:search:/search/tweets', dict)

    logger.info('api limit - {remaining}/{limit} (reset to {reset})'.format_map(api_limit))

    is_final = False

    while 1:
        i = next(c)

        json_tweets = []
        json_comments = []
        json_media = []

        logger.info(f'get {num_posts} tweets <page {i:04d} - next id : {next_id}> : {query}')
        results = get_searched_tweet(client, query, num_posts, next_id)

        if not next_id:
            next_id = 'first'
        try:
            tweets = results['statuses']
            meta = results['search_metadata']

        except Exception:
            logger.error('cannot crawl tweet data.')
            logger.critical(f'you can try with next_id : {next_id}')
            break

        save_json('twit', query, 'list', tweets, next_id, i, True)

        for tweet in tweets:
            # get_twitter_twit(tweet, jsonResult)
            add_list(json_tweets, get_custom_post(tweet))
            add_list(json_comments, get_custom_comment(tweet))
            add_list(json_media, get_custom_media(tweet))

        logger.info('save scrap data')

        save_json('twit', query, 'post', json_tweets, next_id, i)
        save_json('twit', query, 'comment', json_comments, next_id, i)
        save_json('twit', query, 'media', json_media, next_id, i)

        next_results = meta.get('next_results', None)
        if next_results:
            next_id = parse.parse_qs(next_results[1:])['max_id'][0]
        else:
            is_final = True

        if is_final:
            logger.info('final page crawled')
            next_id = None
            break

    logger.info('search "{}" SAVED'.format(query))

    if next_id == 'first':
        next_id = None
    return next_id


if __name__ == '__main__':
    search_query('신발')
