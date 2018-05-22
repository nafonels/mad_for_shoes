import json
from itertools import count
from urllib import parse

import oauth2
from datetime import datetime, timedelta

from config import twitter_consumer_key, twitter_consumer_secret, \
    twitter_access_token, twitter_access_secret


def oauth2_request(consumer_key, consumer_secret,
                   access_token, access_secret):
    try:
        consumer = oauth2.Consumer(key=consumer_key,
                                   secret=consumer_secret)
        token = oauth2.Token(key=access_token,
                             secret=access_secret)
        client = oauth2.Client(consumer, token)
        return client

    except Exception as e:
        print(e)
        return None


def get_user_timeline(client, search_query, count=50, max_id=None):
    base = "https://api.twitter.com/1.1/"
    node = "search/tweets.json"
    field = {
        'q': search_query,
        'count': count,
        'max_id': max_id,
    }

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
        tweet_published = tweet_published + timedelta(hours=+9)
        tweet_published = tweet_published.strftime('%Y-%m-%d %H:%M:%S')
    else:
        tweet_published = ''

    num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
    num_comments = 0
    num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
    num_likes = num_favorite_count
    num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

    jsonResult.append({
        'post_id': tweet_id,
        'message': tweet_message,
        'name': screen_name,
        'link': tweet_link,
        'created_time': tweet_published,
        'num_reactions': num_favorite_count,
        'num_comments': num_comments,
        'num_shares': num_shares,
        'num_likes': num_likes,
        'num_loves': num_loves,
        'num_wows': num_wows,
        'num_hahas': num_hahas,
        'num_sads': num_sads,
        'num_angrys': num_angrys,
        'hashtags': hashtags
    })

    return jsonResult


def main_func(screen_name, num_posts=50):
    jsonResult = []
    next_id=None
    cnt=count(1)
    client = oauth2_request(twitter_consumer_key, twitter_consumer_secret,
                            twitter_access_token, twitter_access_secret)
    while 1:
        tweets = get_user_timeline(client, screen_name, num_posts, next_id)
        # print(tweets)
        i=next(cnt)
        with open('temp%d.json' %i, 'w') as fp:
            fp.write(json.dumps(tweets, indent=4))

        meta = tweets['search_metadata']
        next_id = parse.parse_qs(meta['next_results'][1:])['max_id']
        print(next_id)
    # for tweet in tweets:
    #     get_twitter_twit(tweet, jsonResult)
    #
    # file_name = f"{screen_name}_twitter.json"
    # with open(file_name, 'w', encoding='utf-8') as outfile:
    #     str_ = json.dumps(jsonResult,
    #                       indent=4, sort_keys=True,
    #                       ensure_ascii=False)
    #     outfile.write(str_)
    #
    # print('{} SAVED'.format(screen_name))


if __name__ == '__main__':
    main_func('jtbc_news')
