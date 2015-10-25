#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
from yelpapi import YelpAPI
from pprint import pprint
import sys
import json
settings = {
    'consumer_key' : 'w5aWv_7L5_pAPNrTXR6wZA',
    'consumer_secret' : 'gezgXYOj94qtTZKhLSXLJf3qNF0',
    'token' : 'uSbFcPHea-AMirQLJaf-KxQuGJOUilK-',
    'token_secret' : 'wOOZcevp_BTz2GucqfkEli-oYRQ'
}

yelp_api = YelpAPI(settings['consumer_key'],
                   settings['consumer_secret'],
                   settings['token'],
                   settings['token_secret'])
response = yelp_api.search_query(location='madrid, spain', sort=2, limit=5)

print type(response)
print response.keys()
print len(response['businesses'])
