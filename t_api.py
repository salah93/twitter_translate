import json
import os
import re
import urllib
import oauth2 as oauth


def oauth_req(consumer_key, consumer_secret, key, secret):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    return client


def search_hashtag(client, hashtag, since_id='0'):
    hashtag = urllib.urlencode({'q': hashtag, 'since_id': since_id})
    url = 'https://api.twitter.com/1.1/search/tweets.json?%s' % hashtag
    resp, content = client.request(url, method='GET', body='', headers=None)
    assert resp.status == 200
    return content


def reply_to_user(client, tweet_id, status):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    resp, content = client.request(url, method='POST', body='in_reply_to_status_id=%s&status=%s' % (tweet_id, status), headers=None)


def get_text_and_user(client, content):
    hashtags_regex = re.compile('#\w+')
    for i in content['statuses']:
        tweet_id = i['id']
        body = ' '.join(hashtags_regex.split(i['text'])).strip()
        print body
        status = 'translating "%s" ... v2' % body
        reply_to_user(client, tweet_id, status)


if __name__ == '__main__':
    consumer_key = os.environ['twitter_consumer_key']
    consumer_secret = os.environ['twitter_consumer_secret']
    access_token = os.environ['twitter_access_token']
    access_token_secret = os.environ['twitter_access_token_secret']
    client = oauth_req(consumer_key, consumer_secret, access_token, access_token_secret)
    content = json.loads(search_hashtag(client, '#translate_salah'))
    since_id = content['search_metadata']['max_id_str']
    get_text_and_user(client, content)
    content = json.loads(search_hashtag(client, '#translate_salah', since_id))
    get_text_and_user(client, content)
