import json
import os
import re
import urllib

import oauth2 as oauth
import requests
from bs4 import BeautifulSoup
from google.cloud import translate
try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser


def oauth_req(consumer_key, consumer_secret, key, secret):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    return client


def search_hashtag(hashtag, since_id='0'):
    hashtag = urllib.urlencode({'q': hashtag, 'since_id': since_id})
    url = 'https://api.twitter.com/1.1/search/tweets.json?%s' % hashtag
    resp, content = client.request(url, method='GET', body='', headers=None)
    assert resp.status == 200
    return content


def reply_to_user(tweet_id, status):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    body = 'in_reply_to_status_id=%s&status=%s' % (tweet_id, status)
    resp, content = client.request(url, method='POST', body=body, headers=None)
    from IPython import embed; embed()


def get_text_and_user(content):
    hashtags_regex = re.compile('#\w+')
    results = []
    # Instantiates a client
    translate_client = translate.Client()
    for i in content['statuses']:
        user = i['user']['screen_name']
        tweet_id = i['id']
        body = ' '.join(hashtags_regex.split(i['text'])).strip()
        results.append((user, body))
        # translation begins

        # The text to translate
        # The target language
        target = 'es'
        # Translates some text into Spanish
        response = translate_client.translate(
            body,
            target_language=target)
        translation = html_parser.unescape(response['translatedText'])
        print(u'Text: {}'.format(body))
        print(u'Translation: {}'.format(translation))
        # translation complete
        reply_to_user(tweet_id, translation)
    return results


if __name__ == '__main__':
    html_parser = HTMLParser()
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    client = oauth_req(consumer_key, consumer_secret, access_token, access_token_secret)
    content = json.loads(search_hashtag('#translate_salah'))
    since_id = content['search_metadata']['max_id_str']
    get_text_and_user(content)
    content = json.loads(search_hashtag('#translate_salah', since_id))
    results = get_text_and_user(content)
    for i in results:
        print("user: %s\ntweet: %s\n\n" % (i[0], i[1]))
