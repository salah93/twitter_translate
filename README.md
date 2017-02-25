# Translate Bot
A twitter bot that translates tweets !@!@!!

## what you'll learn
+ twitter api
+ google translate api
+ crontab
+ mailx
+ redis

## Steps
1. clone repo
    ```
    git clone https://github.com/salah93/twitter_translate
    cd twitter_translate
    ```

2. create virtualenv, install pip packages
    ```
    pip install -U pip
    pip install virtualenv
    mkdir ~/.virtualenvs
    virtualenv ~/.virtualenvs/twitBot
    . ~/.virtualenvs/twitBot/bin/activate
    pip install -r requirements.txt
    ```

3. set up twitter api
    - create a new [twitter application](https://apps.twitter.com/)
    - save consumer key, consumer secret, access  key and access secret as environment variables
    ```
    export TWITTER_CONSUMER_KEY='aaaaaaaaaaaaaaaaaaaaaaaaa'
    export TWITTER_CONSUMER_SECRET='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    export TWITTER_ACCESS_TOKEN='aaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    export TWITTER_ACCESS_TOKEN_SECRET='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    ```
4. set up google translate api
    - follow the steps [here](https://cloud.google.com/translate/docs/getting-started)
    - for step 5 set up [service account](https://cloud.google.com/speech/docs/common/auth#set_up_a_service_account)
        - following the steps, you should have set up environment variable pointing to service account file
        ```
        export GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
        ```

5. add environment variables
    + add those previous environment variables to your ~/.bashrc for continuous use in later sessions

6. set up redis
    + using `tmux` create a new session
    + using your system's package manager, install redis (fedora=dnf, ubuntu=apt-get, mac-os=brew?)
    + start redis server
    ```
    sudo dnf install -y tmux
    tmux
    sudo dnf install -y redis
    redis-server
    <ctrl-b> d
    ```

7. Test app
    + change hashtag to whatever you want your app to look for, tweet then test app
    ```
    python translate_bot.py
    ```

8. set up [mailx](https://coderwall.com/p/ez1x2w/send-mail-like-a-boss)
9. set up [crontab](http://kvz.io/blog/2007/07/29/schedule-tasks-on-linux-using-crontab/)
```
crontab -e
SHELL=/bin/bash
0 8-23 * * * . ~/.bashrc; ~/.virtualenvs/twitter3/bin/python ~/Projects/twitter_translate/translate_bot.py 2>&1 | mail -A gmail -s "Twitter Translation output" youremail@gmail.com
```
