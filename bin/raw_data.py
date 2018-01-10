import json
import requests

import pymongo
from pymongo import MongoClient
import numpy
import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.utcnow()

import facebook

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

all_restaurants = db.all_restaurants

restaurants = list(all_restaurants.find({'score': 0}))

# pp.pprint(restaurants)

none_list = [x for x in restaurants if len(x['checkins']) < 14]

pp.pprint(none_list)
# from IPython import embed; embed()
# for fin in none_list:
# 	all_restaurants.update_one({'yelpId': final['yelpId']},
# 		{"$set":fin})