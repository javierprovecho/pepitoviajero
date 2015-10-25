#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
import datetime
import tweepy
import os
import re
import sys

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
    print "TWEET:"
    for attr in json_input:
        hash_str = "{}:{}".format(attr, json_input[attr])
        if hash_str not in buff:
            buff.add(hash_str)
            status = getTweet(attr, json_input[attr], delta_dict)
            if status is not None:
                if len(status) < 135:
                    status += "{}".format(uuid.uuid1())
                    tweetStatus(api, status)

def getTweet(attr, value, delta):
    attr = attr.encode('ascii', 'ignore').lower().strip()
    if delta != 0:
        return None

    try:
        if int(delta) <= 30:
            return None
    except:
        pass
    if attr == "city":
        return "#{} Un nuevo sitio por descubrir.".format(value)
    elif attr == "temperature":
        if value < 19:
            return "Que Frio!!! {} grados C".format(int(value))
        elif  value >= 25:
            return "Que Calor {} grados C".format(int(value))
        elif delta > 10:
            return "Que cambio tan brusco de temperatura.".format(int(value))
    elif attr == "time":
        if value == "dia":
            return "Que tengan un buen dia."
        elif value == "tarde":
            return "Buenas tardes."
        elif value == "noche":
            return "Buenas Noches"
    elif attr == "luminance":
        if value <= 3:
            return "Que Oscuro!! No veo nada"
        if delta >= 50:
            return "Que haya LUZ!!"
    elif attr == "battery":
        if value <= 30:
            return "Ayudadme se me acaba la bateria!! {}%".format(value)
        if value <= 5:
            return "Adios mundo cruel. Solo {}% de bateria"
        return "UUfff {}% de bateria.".format(value)
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
