# Translate Bot
A twitter bot that translates tweets !@!@!!

## what you'll learn
+ twitter api
+ google translate api
+ crontab
+ mailx
+ redis

## Steps
1. create virtualenv, install pip packages
```
pip install -U pip
pip install virtualenv
mkdir ~/.virtualenvs
virtualenv ~/.virtualenvs/twitBot
. ~/.virtualenvs/twitBot/bin/activate
pip install -r requirements.txt
```

1. set up twitter api
    - create a new [twitter application](https://apps.twitter.com/)
    - save consumer key, consumer secret, access  key and access secret as environment variables
```
export TWITTER_CONSUMER_KEY='aaaaaaaaaaaaaaaaaaaaaaaaa'
export TWITTER_CONSUMER_SECRET='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
export TWITTER_ACCESS_TOKEN='aaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
export TWITTER_ACCESS_TOKEN_SECRET='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
```
2. set up google translate api
    - follow the steps [here](https://cloud.google.com/translate/docs/getting-started)
    - for step 5 set up [service account](https://cloud.google.com/speech/docs/common/auth#set_up_a_service_account)
        - following the steps, you should have set up environment variable pointing to service account file
```
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
```

3. add environment variables
    + add those previous environment variables to your ~/.bashrc for continuous use in later sessions

4. set up redis
    + open a new terminal
    + using your system's package manager, install redis (fedora=dnf, ubuntu=apt-get, mac-os=brew?)
    + start redis server
```
sudo dnf install -y redis
redis-server
```

6. change hashtag to whatever you want your app to look for, tweet then test app
```
python translate_bot.py
```

5. set up mailx
6. set up crontab
