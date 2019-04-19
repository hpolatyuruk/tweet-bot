import os
import time
import random
import tweepy
import datetime
from configparser import ConfigParser

def get_tokens(filename = os.path.join(os.getcwd(), 'tokens.ini'), section = 'tokens'):
    parser = ConfigParser()
    parser.read(filename)
    print(filename)
    # get section, default to tokens

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

tokens = get_tokens()

if len(tokens['consumer_key']) == 0:
    print('Please enter your app consumer key.')
    exit()
if len(tokens['consumer_secret']) == 0:
    print('Please enter your app consumer secret.')
    exit()
if len(tokens['access_key']) == 0:
    print('Please enter your app access token key.')
    exit()
if len(tokens['access_secret']) == 0:
    print('Please enter your app access secret.')
    exit()

auth = tweepy.OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
auth.set_access_token(tokens['access_key'], tokens['access_secret'])

api = tweepy.API(auth)

# put your tweets into this list
tweets = []

if len(tweets) == 0:
    print('Empty tweet list. Please enter at least one tweet.')
    exit()

last_tweet_index = 0
tweet_indexes = list(range(0, len(tweets)))

while True:
    try:     
        tweet_index = random.choice(tweet_indexes)
        api.update_status(tweets[tweet_index])

        # twitter doesn't allow us to tweet same status in same day
        # therefore we remove the already tweet from list to skip it
        tweet_indexes.remove(tweet_index)

        # refill the list to start from scratch to tweet them all for new day
        if len(tweet_indexes) == 0:
            tweet_indexes = list(range(0, len(tweets)))

        # change tweet frequency here (every 3hours by default)
        time.sleep(10800)
    except tweepy.error.TweepError as err:
        print(err)
    