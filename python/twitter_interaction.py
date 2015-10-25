#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
import tweepy
import json

CONSUMER_KEY = 'OLcBTV6Urgh9OJ9IfUzSG0wmX'
CONSUMER_SECRET = 'SSHFdKDjhuZGMNwMxufeXcvXb1okU4mQSwUFZRkhythPMnF4mn'
ACCESS_TOKEN = '4030796099-7ZNCBg9E6Az9csFrpDtMvMAgjN0xlmelRaLdive'
ACCESS_TOKEN_SECRET = 'FiTnpc78a9LB1iq3v3kqwcjnF1DqDodhz5NQW0RQ9jmCK'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#api = tweepy.API(auth)

#status = "Testing!"
#api.update_status(status=status)
# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print "Error:"
        print status

if __name__ == '__main__':
    l = StdOutListener()

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    #stream.filter(track=['the'])
    stream.filter(follow=None, locations=[-122.75,36.8,-121.75,37.8])
    #stream.filter(follow=None, locations=[40.41549, -3.70739, 40.4192536, -3.6974721])

