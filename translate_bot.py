import json
import os
import re
try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
    from urllib import urlencode
except ImportError:
    # Python 3
    from html.parser import HTMLParser
    from urllib.parse import urlencode

import oauth2 as oauth
import redis

from google.cloud import translate


def oauth_req(consumer_key, consumer_secret, key, secret):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    return client


def search_hashtag(hashtag, since_id='0'):
    hashtag = urlencode({'q': hashtag, 'since_id': since_id})
    url = 'https://api.twitter.com/1.1/search/tweets.json?%s' % hashtag
    resp, content = client.request(url.encode('ascii'), method='GET', body=''.encode('utf-8'), headers=None)
    assert resp.status == 200
    return content.decode('utf-8')


def split_tweet(tweet):
    ''' in case tweet exceeds 140 characters '''
    if tweet == '':
        return []
    return [tweet[:TWITTER_MAX - 10]] + split_tweet(tweet[TWITTER_MAX - 10:])


def reply_to_user(tweet_id, status):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    tweets = list(filter(lambda x: x, split_tweet(status)))
    for t in tweets:
        body = 'in_reply_to_status_id=%s&status=%s' % (tweet_id, t)
        # resp, content = client.request(url, method='POST', body=body, headers=None)
    return tweets


def get_text_and_user(content):
    hashtags_regex = re.compile('#\w+')
    users_regex = re.compile('@\w+')
    results = []
    # Instantiates a client
    translate_client = translate.Client()
    for i in content['statuses']:
        user = i['user']['screen_name']
        tweet_id = i['id']
        body = ' '.join(users_regex.split(' '.join(hashtags_regex.split(i['text'])).strip())).strip()
        if not body:
            in_reply = i['in_reply_to_status_id']
            if not in_reply:
                continue
            url = 'https://api.twitter.com/1.1/statuses/show.json?id=%s' % in_reply
            response, content = client.request(url, method='GET', body=''.encode('utf-8'), headers=None)
            tweet = json.loads(content.decode('utf-8'))
            body = ' '.join(
                    users_regex.split(
                        ' '.join(hashtags_regex.split(tweet['text'])).strip())).strip()
            if not body:
                continue
        # translation begins

        # The text to translate
        # The target language
        target = 'es'
        # Translates some text into Spanish
        response = translate_client.translate(
            body,
            target_language=target)
        translation = html_parser.unescape(response['translatedText'])
        # translation complete
        tweets = reply_to_user(tweet_id, translation)
        results.append(dict(user=user, text=body, translation=tweets))
    return results


if __name__ == '__main__':
    TWITTER_MAX = 140
    html_parser = HTMLParser()
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    client = oauth_req(consumer_key, consumer_secret, access_token, access_token_secret)
    # get past since_id
    r = redis.StrictRedis()
    since_id = r.get('since_id') or '0'
    content = json.loads(search_hashtag('#translate_salah', since_id))
    # update since_id
    since_id = content['search_metadata']['max_id_str']
    r.set('since_id', since_id)
    results = get_text_and_user(content)
    for tweet in results:
        print(u'User: {}'.format(tweet['user']).encode('utf-8'))
        print(u'Text: {}'.format(tweet['text']).encode('utf-8'))
        print(u'Translation: {}'.format(tweet['translation']).encode('utf-8'))
