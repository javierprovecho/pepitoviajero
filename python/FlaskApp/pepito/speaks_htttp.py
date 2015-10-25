#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
from pprint import pformat, pprint
from pepito import twitea
import random
import requests
import sys


headers = {
    'Accept' : 'application/json',
    'Fiware-Service' : 'todosincluidos',
    'Fiware-ServicePath' : '/iot',
}

def generateDict():
    rgb = "{},{},{}".format(random.randint(0,1), random.randint(0,1), random.randint(0,1))
    return {
        'city' : 'Madrid',
        'luminosity' : random.randint(0, 500),
        'battery' : random.randint(0, 100),
        'color': rgb,
        'humidity' : random.randint(0, 100),
        'temperature' : random.randint(0, 40),
        }


def setEmotion(emotion):
    url = 'http://pepitoviajero.herokuapp.com/setcolor'
    emotion_map = twitea.getEmotionMap()
    rgb = emotion_map[emotion]
    rgb = rgb.split(",")
    try:
        p = requests.get(url,
                         headers=headers, params={
                        'red':rgb[0],
                        'green':rgb[1],
                        'blue':rgb[2]})
    except Exception,e:
        return("{} is failing!!!<br>{}".format(url, e))
    return p.url
def getJSONInput():
    url = 'http://pepitoviajero.herokuapp.com/all'
    try:
        p = requests.get(url, headers=headers)
    except Exception,e:
        return("{} is failing!!!<br>{}".format(url, e))
    if p is not None:
        try:
            json_input = json.loads(p.text)
            return json_input
        except Exception,e:
            print("Is NOT JSON:\n {}<br>{}".format(p.text, e))
    return None

#def run(sensor_buffer, tweets_buffer, api, previous_dict, delta_dict={}):
def run(api, buffers_dict, delta_dict={}):
    sensor_buffer = buffers_dict['sensor_buffer']
    tweets_buffer = buffers_dict['tweets_buffer']
    previous_dict = buffers_dict['previous_dict']
    #json_input = getJSONInput()
    json_input = generateDict()
    if json_input is not None:
        if 'message' in json_input:
            return "=(<br>message:<br>{}".format(json_input["message"])
        json_input = twitea.addContext(json_input)
        if len(previous_dict) == 0:
            for attr in json_input:
                previous_dict[attr] = json_input[attr]
                delta_dict[attr] = json_input[attr]
        else:
            for attr in json_input:
                try:
                    delta_dict[attr] = abs(json_input[attr] - previous_dict[attr])
                    delta_dict[attr] = float(delta_dict[attr])/float(json_input[attr])
                    delta_dict[attr] = int(delta_dict[attr]*100)
                except:
                    try:
                        if previous_dict[attr] != json_input[attr]:
                            delta_dict[attr] = json_input[attr]
                        else:
                            delta_dict[attr] = 0
                    except:
                        delta_dict[attr] = 0
                previous_dict[attr] = json_input[attr]
        twitea.tweetNewValues(json_input, delta_dict, sensor_buffer, api)
    else:
        return "Thinking Things Says: <br>{}".format(p)
    return "<h1>It WORKS!</h1>"

