__author__ = 'Nycidian'


# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from libavg import app, avg
import json
from pprint import pprint
import urllib

with open('json/tree.json') as data_file:
    tree = json.load(data_file)

imageRoot = tree['imageRoot']


"""
for value in tree['nodes']:
    print(imageRoot[:-1]+value['icon'])
    name = value['icon'].split('/')
    print(name[-1])
    urllib.urlretrieve(imageRoot[:-1]+value['icon'], 'downloaded/'+name[-1])
"""