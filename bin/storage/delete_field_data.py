import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.utcnow()

import facebook

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)


all_restaurants = db.all_restaurants

allrest = (list(all_restaurants.find()))
# gets data from all_ids. adds initial data
# allids = list(all_ids.find())
restaurants = list(all_restaurants.find({
	'checkins': {
		'$elemMatch': {
			'query_date': {
				'$regex': '2017-12-27 05:48:35.033732'
			}
		}
	}
	})
)
pp.pprint(len(restaurants))
for each in restaurants:
	each['checkins'] = [x for x in each['checkins'] if x['query_date'] != '2017-12-27 05:48:35.033732' if x['query_date'] != '2017-12-27 16:45:10.762218']
	each['rating_count'] = [x for x in each['rating_count'] if x['query_date'] != '2017-12-27 05:48:35.033732' if x['query_date'] != '2017-12-27 16:45:10.762218']
	each['reviews'] = [x for x in each['reviews'] if x['query_date'] != '2017-12-27 05:48:35.033732' if x['query_date'] != '2017-12-27 16:45:10.762218']

pp.pprint(restaurants)

for each in restaurants:
	all_restaurants.update_one({'yelpId': each['yelpId']},
		{'$set': each}
	)
pp.pprint(allrest)
from IPython import embed; embed()