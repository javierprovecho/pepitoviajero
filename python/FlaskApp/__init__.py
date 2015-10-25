
from flask import Flask
from pprint import pformat, pprint
import tweepy
import os
import re
import sys
import cPickle as pickle
import datetime
import requests
import json
import uuid
import random
from pepito import twitea, speaks_htttp
BUFFER_SIZE = 1000
fileDict = {
    'sensor_buffer' : '/tmp/pepito-app.pckl',
    'tweets_buffer' : '/tmp/pepito-tweets.pckl',
    'previous_dict' : '/tmp/pepito-previous.pckl'
}
initialBuff = {
    'sensor_buffer' : set(),
    'tweets_buffer' : set(),
    'previous_dict' : {}
}

def serializeBuffers(buffers_dict):
    for buff in buffers_dict:
        buff_file = fileDict[buff]
        pickle.dump(buffers_dict[buff], open(buff_file, 'wb'))

def initializeBuffers():
    initializedBuffs = {}
    for buff in fileDict:
        buff_file = fileDict[buff]
        if os.path.exists(buff_file):
            with open(buff_file,'rb') as fp:
                deserialized_buff = pickle.load(fp)
                if len(deserialized_buff) >= BUFFER_SIZE:
                    initializedBuffs[buff] = initialBuff[buff]
                else:
                    initializedBuffs[buff] = deserialized_buff
        else:
            initializedBuffs[buff] = initialBuff[buff]
    return initializedBuffs

app = Flask(__name__)

@app.route("/")
def incoming():
    print "\n\nINCOMING\n\n"
    buffers_dict = initializeBuffers()
    try:
        api = twitea.getTwitterAPI()
    except Exception, e:
        return str(e)

    try:
        speaks_htttp.run(api, buffers_dict)
        #return speaks_htttp.setEmotion('enfadado')
        #return speaks_htttp.setEmotion('triste')

        #return run(url+'all', sensor_buffer, tweets_buffer, api, previous_dict)
        #return setEmotion(url+'setcolor', 'triste')
    finally:
        serializeBuffers(buffers_dict)
    return "<h1>It Works!</h1>"
if __name__ == "__main__":
    app.debug = True
    #app.run(port=6868, host="0.0.0.0")
    app.run(port=6868)
