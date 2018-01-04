import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.utcnow()

import urllib3
import facebook

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

all_restaurants = db.all_restaurants
restaurants = list(all_restaurants.find())

ids = []
for each in restaurants:
	ids.append({
		'fbId':each['fbId'],
		'yelpId': each['yelpId']
	})

all_ids = db.all_ids

for data in ids:
	all_ids.update_one(
		{'fbId': data['fbId']},
		{'$set': data},
		upsert=True
	)
print(all_ids.count())
# from IPython import embed; embed()

