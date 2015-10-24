#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""

import requests

url = 'http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW'
headers = {
        'Accept' : 'application/json',
           'Fiware-Service' : 'todosincluidos',
          'Fiware-ServicePath' : '/iot',
          }
p = requests.get(url, headers=headers)
print(p.url)
print(p.text)

