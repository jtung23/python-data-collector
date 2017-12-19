#!/usr/bin/env python

import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.now()

import urllib3
import facebook

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

fb_restaurants = db.Fbrestaurants

restaurants = list(fb_restaurants.find())

access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)

new_data = []
for item in restaurants:
	place_id = item['fbId']
	search_link= place_id + '?fields=name,rating_count,checkins'
	restaurants = graph.request(search_link)
	place_list= restaurants
	new_data.append(restaurants)

for item in new_data:
	fb_restaurants.find_one_and_update({
		'fbId': item['id']
	},
	{
		'$push': {
			'rating_count': {
				'rating_count': item['rating_count'],
				'query_date': str(now)
			}
		}
	})

print('done')