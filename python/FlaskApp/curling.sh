#! /bin/sh
#
# curling.sh
# Copyright (C) 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.
#

for i in `seq 1 100`;
  do
    echo $i
    curl http://localhost:6868/;
    sleep 3s;
  done
