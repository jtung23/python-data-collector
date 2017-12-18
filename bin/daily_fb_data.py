#!/usr/bin/env python

import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.now()

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

# Updates yelpId database based on id_arrays.json
jsondata = json.load(open('id_arrays.json'))

yelp_ids = jsondata['yelpArrIds']

yelpIds = db.yelpIds
for doc in yelp_ids:
	yelpIds.update_one({'yelpId': doc['yelpId']},
		{"$set":doc}, upsert=True)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

items = list(yelpIds.find())
my_list = []

2 month user access token
EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD