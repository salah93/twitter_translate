import json
import os
import re
import urllib

import oauth2 as oauth
import requests
from bs4 import BeautifulSoup


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
    resp, content = client.request(url, method='POST', body='in_reply_to_status_id=%s&status=%s' % (tweet_id, status), headers=None)


def get_text_and_user(content):
    hashtags_regex = re.compile('#\w+')
    results = []
    for i in content['statuses']:
        user = i['user']['screen_name']
        tweet_id = i['id']
        body = ' '.join(hashtags_regex.split(i['text'])).strip()
        print body
        results.append((user, body))
        url = 'http://www.spanishdict.com/translate/%s'
        url = url % urllib.quote(body)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        status = soup.find(class_='lang')
        if not status:
            status = "sorry dude page won't let me scrape :("
        else:
            status = status.text.strip()
        assert status
        reply_to_user(tweet_id, status)
    return results


if __name__ == '__main__':
    consumer_key = os.environ['twitter_consumer_key']
    consumer_secret = os.environ['twitter_consumer_secret']
    access_token = os.environ['twitter_access_token']
    access_token_secret = os.environ['twitter_access_token_secret']
    client = oauth_req(consumer_key, consumer_secret, access_token, access_token_secret)
    content = json.loads(search_hashtag('#translate_salah'))
    since_id = content['search_metadata']['max_id_str']
    get_text_and_user(content)
    content = json.loads(search_hashtag('#translate_salah', since_id))
    results = get_text_and_user(content)
    for i in results:
        print("user: %s\ntweet: %s\n\n" % (i[0], i[1]))
