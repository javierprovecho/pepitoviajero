#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
import time
import unirest
import json
import tweepy
import sys
from pprint import pformat
import requests
import os
import cPickle as pickle
import re

sleep_time = 3
usuario = "@elviajedepepito"
hola_regex = re.compile(r'hola')
SENSOR_BUFFER_SIZE = 10
url = 'http://pepitoviajero.herokuapp.com/all'
headers = {
        'Accept' : 'application/json',
           'Fiware-Service' : 'todosincluidos',
          'Fiware-ServicePath' : '/iot',
          }

def transform(json_input):
    color = []
    for element in json_input['color'].split(','):
        color.append(int(element))
    json_input['color'] = tuple(color)

    json_input['luminance'] = float(json_input['luminance'])
    json_input['humidity'] = int(json_input['humidity'])
    json_input['temperature'] = float(json_input['temperature'])

    coord = (float(json_input['latitude']), float(json_input['longitude']))
    json_input['coordinates'] = coord


def tweet(tweet_string, api):
    #tweet = tweet_string[:120]
    print("TWEET:\n{}".format(tweet_string))
    """
    try:
        api.update_status(status=tweet)
    except Exception,e:
        print("\t{}".format(str(e)))
    """
def tweetDelta(tweet_string, input_string, buffer):
    if len(buffer) == SENSOR_BUFFER_SIZE:
        # RESET sensor_buffer.
        buffer = set()
    if input_string not in buffer:
        buffer.add(input_string)
        tweet(tweet_string)
    else:
        print("\tNo change")

def run(sensor_buffer, tweets_buffer, api):
    # Get the User object for twitter...
    user = api.get_user(usuario)
    print '@{}'.format(user.screen_name)
    #print getRecentTweets(api, user.id)
    while True:
        print 'tasks done, now sleeping for {} seconds'.format(sleep_time)
        for i in xrange(sleep_time, 0, -1):
            sys.stdout.write('\r'+str(i)+' ')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\n')
        # Sensors
        try:
            p = requests.get(url, headers=headers)
        except Exception,e:
            print("{} is failing!!!".format(url))
            continue
        try:
            json_input = json.loads(p.text)
        except Exception,e:
            print("Is NOT JSON:\n {}".format(p.text))
            continue
        transform(json_input)
        pformat(json_input)
        tweetDelta(pformat(json_input), p.text, sensor_buffer)
        """
        # New Tweets
        #pepito_tweets = api.user_timeline(id=user.id,count=5)
        # Only iterate through the first 200 statuses
        for tweet_object in tweepy.Cursor(api.search, q="@elviajedepepito").items(200):
            print(type(tweet_object))
            try:
                tweet_string = tweet_object.text.encode('ascii', 'ignore')
            except Exception,e:
                print("BAD ENCODING IN: \n {}".format(tweet_string))
                continue
            print tweet_string
            if hola_regex.match(tweet_string.lower()):
                print(format(tweet_string))
                #tweetDelta(tweet_string, tweet_string, tweets_buffer)
        sys.exit()
        """


if __name__ == "__main__":
    json_dump_file = '/tmp/pepito-app.pckl'
    tweets_dump_file = '/tmp/pepito-tweets.pckl'
    CONSUMER_KEY = 'OLcBTV6Urgh9OJ9IfUzSG0wmX'
    CONSUMER_SECRET = 'SSHFdKDjhuZGMNwMxufeXcvXb1okU4mQSwUFZRkhythPMnF4mn'
    ACCESS_TOKEN = '4030796099-7ZNCBg9E6Az9csFrpDtMvMAgjN0xlmelRaLdive'
    ACCESS_TOKEN_SECRET = 'FiTnpc78a9LB1iq3v3kqwcjnF1DqDodhz5NQW0RQ9jmCK'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets_buffer = set()
    sensor_buffer = set()
    if os.path.exists(json_dump_file):
        with open(json_dump_file,'rb') as fp:
            sensor_buffer = pickle.load(fp)
    if os.path.exists(tweets_dump_file):
        with open(tweets_dump_file, 'rb') as fp:
            tweets_buffer = pickle.load(fp)
    try:
        run(sensor_buffer, tweets_buffer, api)
    finally:
        pickle.dump(sensor_buffer, open(json_dump_file, 'wb'))
        pickle.dump(tweets_buffer, open(tweets_dump_file, 'wb'))
