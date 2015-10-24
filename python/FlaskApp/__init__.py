
from flask import Flask
from pprint import pformat
import tweepy
import os
import re
import sys
import cPickle as pickle
import datetime
import requests
import json
import uuid
USUARIO = "@elviajedepepito"
BUFFER_SIZE = 1000
hola_regex = re.compile(r'hola')
url = 'http://pepitoviajero.herokuapp.com/'

headers = {
        'Accept' : 'application/json',
           'Fiware-Service' : 'todosincluidos',
          'Fiware-ServicePath' : '/iot',
          }
color_map = {'1,0,1' : 'enamorado',
             '1,0,0' : 'enfadado',
             '0,0,1' : 'triste',
             '0,1,0' : 'asqueado',
             '1,1,0' : 'alegre',
             '0,0,0' : 'apagado',
             '0,1,1' : 'asustado',
             '1,1,1' : 'encendido'
        }
             
emotion_map = {}
for rgb in color_map:
    emotion_map[color_map[rgb]] = rgb
def setEmotion(url, emotion):
    rgb = emotion_map[emotion]
    rgb = rgb.split(",")
    try:
        p = requests.get(url, headers=headers, params={'red':rgb[0],
            'green':rgb[1],
            'blue':rgb[2]})
    except Exception,e:
        return("{} is failing!!!<br>{}".format(url, e))
    return p.url
      
app = Flask(__name__)
def run(url, sensor_buffer, tweets_buffer, api, previous_dict, delta_dict={}):
    p = None
    # Sensors
    try:
        p = requests.get(url, headers=headers)
    except Exception,e:
        return("{} is failing!!!<br>{}".format(url, e))
    if p is not None:
        try:
            json_input = json.loads(p.text)
        except Exception,e:
            return("Is NOT JSON:\n {}<br>{}".format(p.text, e))

        if 'message' in json_input:
            return "=(<br>message:<br>{}".format(json_input["message"])
        hour = datetime.datetime.now().hour
        if hour < 12:
            json_input['time'] = "dia" 
        elif hour >= 12 and hour <= 6:
            json_input['time'] = "tarde" 
        else:
            json_input['time'] = "noche" 

        json_input['emocion'] = color_map[json_input['color']]
        print "EMOCION: {}".format(json_input['emocion'])
        if len(previous_dict) == 0:
            for attr in json_input:
                previous_dict[attr] = json_input[attr] 
        else:
            for attr in json_input:
                try:
                    delta_dict[attr] = abs(json_input[attr] - previous_dict[attr])
                    delta_dict[attr] /= json_input[attr]
                    delta_dict[attr] = int(delta_dict[attr])
                    print "Delta: \n {}:{}".format(attr, delta_dict[attr])
                except:
                    try:
                        if previous_dict[attr] != json_input[attr]:
                            delta_dict[attr] = json_input[attr]
                        else:
                            delta_dict[attr] = 0
                    except:
                        delta_dict[attr] = 0
                previous_dict[attr] = json_input[attr]
        tweetNewValues(json_input, delta_dict, sensor_buffer, api)
    else:
        return "Thinking Things Says: <br>{}".format(p)
    return "<h1>It WORKS!</h1>"
def tweetStatus(api, status):
    cropped_status = status[:140]
    print("\t{}".format(cropped_status))
    """
    try:
        api.update_status(status=cropped_status)
    except Exception,e:
        print("\t{}".format(str(e)))
    """

def getTweet(attr, value, delta):
    attr = attr.encode('ascii', 'ignore').lower().strip()
    if delta == 0:
        return None
    
    if attr == "city":
        return "#{} Un nuevo sitio por descubrir.".format(value)
    elif attr == "temperature":
        if value < 19:
            return "Que Frio!!! {} grados C".format(int(value))
        elif  value >= 25:
            return "Que Calor {} grados C".format(int(value))
        elif delta > 10:
            return "Que Calor!! {} grados C".format(int(value))
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
        if delta >= 10:
            return "Que haya LUZ!!"
    elif attr == "battery":
        if value <= 30:
            return "Ayudadme se me acaba la bateria!! {}%".format(value)
        if value <= 5:
            return "Adios mundo cruel. Solo {}% de bateria"

        return "UUfff {}% de bateria.".format(value)
    return None 
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
@app.route("/")
def incoming():
    print "\n\nINCOMING\n\n"
    json_dump_file = '/tmp/pepito-app.pckl'
    tweets_dump_file = '/tmp/pepito-tweets.pckl'
    previous_dump_file = '/tmp/pepito-previous.pckl'
    CONSUMER_KEY = 'OLcBTV6Urgh9OJ9IfUzSG0wmX'
    CONSUMER_SECRET = 'SSHFdKDjhuZGMNwMxufeXcvXb1okU4mQSwUFZRkhythPMnF4mn'
    ACCESS_TOKEN = '4030796099-7ZNCBg9E6Az9csFrpDtMvMAgjN0xlmelRaLdive'
    ACCESS_TOKEN_SECRET = 'FiTnpc78a9LB1iq3v3kqwcjnF1DqDodhz5NQW0RQ9jmCK'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweets_buffer = set()
    sensor_buffer = set()
    previous_dict = {}
    if os.path.exists(json_dump_file):
        with open(previous_dump_file,'rb') as fp:
            previous_dict = pickle.load(fp)
    if os.path.exists(json_dump_file):
        with open(json_dump_file,'rb') as fp:
            sensor_buffer = pickle.load(fp)
    if len(sensor_buffer) >= BUFFER_SIZE:
        sensor_buffer = set()
    if os.path.exists(tweets_dump_file):
        with open(tweets_dump_file, 'rb') as fp:
            tweets_buffer = pickle.load(fp)
    if len(tweets_buffer) >= BUFFER_SIZE:
        sensor_buffer = set()
    try:
        #return run(url+'all', sensor_buffer, tweets_buffer, api, previous_dict)
        return setEmotion(url+'setcolor', 'triste')
    finally:
        pickle.dump(sensor_buffer, open(json_dump_file, 'wb'))
        pickle.dump(tweets_buffer, open(tweets_dump_file, 'wb'))
        pickle.dump(previous_dict, open(previous_dump_file, 'wb'))
if __name__ == "__main__":
    app.debug = True
    app.run(port=6868, host="0.0.0.0")
