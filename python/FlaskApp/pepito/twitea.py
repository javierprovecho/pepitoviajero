#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
from pprint import pprint, pformat
import datetime
import tweepy
import os
import re
import sys
from pepito import text_generators
def getColorMap():
    color_map = {'1,0,1' : 'enamorado',
                 '1,0,0' : 'enfadado',
                 '0,0,1' : 'triste',
                 '0,1,0' : 'asqueado',
                 '1,1,0' : 'alegre',
                 '0,0,0' : 'apagado',
                 '0,1,1' : 'asustado',
                 '1,1,1' : 'encendido'
            }
    return color_map

def getEmotionMap():
    emotion_map = {}
    color_map = getColorMap()
    for rgb in color_map:
        emotion_map[color_map[rgb]] = rgb
    return emotion_map

def getTwitterAPI():
    CONSUMER_KEY = 'OLcBTV6Urgh9OJ9IfUzSG0wmX'
    CONSUMER_SECRET = 'SSHFdKDjhuZGMNwMxufeXcvXb1okU4mQSwUFZRkhythPMnF4mn'
    ACCESS_TOKEN = '4030796099-7ZNCBg9E6Az9csFrpDtMvMAgjN0xlmelRaLdive'
    ACCESS_TOKEN_SECRET = 'FiTnpc78a9LB1iq3v3kqwcjnF1DqDodhz5NQW0RQ9jmCK'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def addContext(json_input):
    hour = datetime.datetime.now().hour
    color_map = getColorMap()
    if hour < 12:
        json_input['time'] = "dia"
    elif hour >= 12 and hour <= 6:
        json_input['time'] = "tarde"
    else:
        json_input['time'] = "noche"

    json_input['emocion'] = color_map[json_input['color']]
    return json_input
def tweetNewValues(json_input, delta_dict, buff, api):
    pprint(json_input)
    print "TWEET:"
    for attr in json_input:
        #hash_str = "{}:{}".format(attr, json_input[attr])
        #if hash_str not in buff:
        #    buff.add(hash_str)

        status = getTweet(attr, json_input[attr], delta_dict[attr])
        if status is not None:
            if len(status) < 135:
                tweetStatus(api, status)

def getTweet(attr, value, delta):
    attr = attr.encode('ascii', 'ignore').lower().strip()
    if delta == 0:
        return None

    try:
        if int(delta) <= 30:
            return None
    except:
        pass
    if attr == "emocion":
        return text_generators.generate(value)
    if attr == "city":
        return text_generators.generate('lugar')+" #{}".format(value)
    elif attr == "temperature":
        if value < 19:
            return text_generators.generate('frio')
        elif  value >= 25:
            return text_generators.generate('calor')
        elif delta > 10:
            return text_generators.generate('brusco')
        return text_generators.generate('normal')
    elif attr == "time":
        return text_generators.generate(value)
    elif attr == "luminance":
        if value <= 3:
            return text_generators.generate('oscuro')
        if delta >= 50:
            return text_generators.generate('luz')
    elif attr == "battery":
        if value < 10:
            return text_generators.generate('baja')+"{}% bat".format(value)
        if value <= 5:
            return text_generators.generate('muy_baja')+"{}% bat".format(value)
        if value >= 90:
            return text_generators.generate('muy_alta')+"{}% bat".format(value)
        if value >= 60 and value >= 40:
            return text_generators.generate('normal')+"{}% bat".format(value)
        return None#"UUfff {}% de bateria.".format(value)
    return None

def tweetStatus(api, status):
    cropped_status = status[:140]
    print("\t{}".format(cropped_status))
    """
    try:
        api.update_status(status=cropped_status)
    except Exception,e:
        print("\t{}".format(str(e)))
    """
