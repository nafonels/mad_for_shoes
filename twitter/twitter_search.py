import json
from itertools import count
from urllib import parse

from datetime import datetime, timedelta

from config import twitter_consumer_key, twitter_consumer_secret, \
    twitter_access_token, twitter_access_secret, data_path
from twitter.oauth import oauth2_request
from twitter.twitter_client import get_twitter_data
from twitter.util import extract_fields, extract_field, add_list


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


def get_twitter_twit(tweet: dict, jsonResult):
    tweet_id = tweet['id']
    tweet_message = '' if 'text' not in tweet.keys() else tweet['text']
    screen_name = '' if 'user' not in tweet.keys() else tweet['user']['screen_name']

    tweet_link = []
    tweet_entities_urls = tweet['entities']['urls']
    if tweet_entities_urls:
        for i, val in enumerate(tweet_entities_urls):
            tweet_link.append(tweet_entities_urls[i]['url'])
        tweet_link = ' '.join(tweet_link)
    else:
        tweet_link = ''

    hashtags = []
    tweet_entities_hashtags = tweet['entities']['hashtags']
    if tweet_entities_urls:
        for i, val in enumerate(tweet_entities_hashtags):
            hashtags.append(tweet_entities_hashtags[i]['text'])
        hashtags = ' '.join(hashtags)
    else:
        hashtags = ''

    if 'created_at' in tweet.keys():
        tweet_published = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_published = tweet_published + timedelta(hours = +9)
        tweet_published = tweet_published.strftime('%Y-%m-%d %H:%M:%S')
    else:
        tweet_published = ''

    num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
    num_comments = 0
    num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
    num_likes = num_favorite_count
    num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

    jsonResult.append({
        'post_id':       tweet_id,
        'message':       tweet_message,
        'name':          screen_name,
        'link':          tweet_link,
        'created_time':  tweet_published,
        'num_reactions': num_favorite_count,
        'num_comments':  num_comments,
        'num_shares':    num_shares,
        'num_likes':     num_likes,
        'num_loves':     num_loves,
        'num_wows':      num_wows,
        'num_hahas':     num_hahas,
        'num_sads':      num_sads,
        'num_angrys':    num_angrys,
        'hashtags':      hashtags
    })

    return jsonResult


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


def main_func(query, num_posts = 100):
    client = oauth2_request(twitter_consumer_key, twitter_consumer_secret,
                            twitter_access_token, twitter_access_secret)

    # tweets = get_searched_tweet(client, query, num_posts)
    # print(type(tweets))
    # print(tweets)

    next_id = None
    c = count(1)

    print(get_rate_limit(client, ['search']))

    json_tweets = []
    json_comments = []
    json_media = []

    while 1:
        results = get_searched_tweet(client, query, num_posts, next_id)
        # print(type(results))
        # print(results)
        tweets = results['statuses']
        meta = results['search_metadata']

        i = next(c)
        with open(data_path + 'raw/' + f'temp{i}.json', 'w', encoding = 'utf-8') as ofp:
            ofp.write(json.dumps(tweets,
                                 indent = 4))
        next_id = parse.parse_qs(meta['next_results'][1:])

        for tweet in tweets:
            # get_twitter_twit(tweet, jsonResult)
            add_list(json_tweets, get_custom_post(tweet))
            add_list(json_comments, get_custom_comment(tweet))
            add_list(json_media, get_custom_media(tweet))

        if i > 10:
            break

    # file_name = f"{query}_twitter"
    # with open(file_name + '.json', 'w', encoding = 'utf-8') as outfile:
    #     str_ = json.dumps(jsonResult,
    #                       indent = 4, sort_keys = True,
    #                       ensure_ascii = False)
    #     outfile.write(str_)

    file_name = f"{query}_twitter_post"
    with open(data_path + file_name + '.json', 'w', encoding = 'utf-8') as outfile:
        str_ = json.dumps(json_tweets,
                          indent = 2,
                          ensure_ascii = False)
        outfile.write(str_)

    file_name = f"{query}_twitter_comment"
    with open(data_path + file_name + '.json', 'w', encoding = 'utf-8') as outfile:
        str_ = json.dumps(json_comments,
                          indent = 2,
                          ensure_ascii = False)
        outfile.write(str_)

    file_name = f"{query}_twitter_media"
    with open(data_path + file_name + '.json', 'w', encoding = 'utf-8') as outfile:
        str_ = json.dumps(json_media,
                          indent = 4,
                          ensure_ascii = False)
        outfile.write(str_)

    print('{} SAVED'.format(query))


if __name__ == '__main__':
    main_func('신발')