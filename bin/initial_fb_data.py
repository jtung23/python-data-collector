#!/usr/bin/env python

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

# for doc in json_go_names:
# 	go_names.update_one({'goName': doc['goName']},
# 		{"$set":doc}, upsert=True)
client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

# Updates yelpId database based on id_arrays.json
# jsondata = json.load(open('/app/bin/id_arrays.json'))

# json_go_names = jsondata['goArrIds']

# go_names = db.goNames
# for doc in json_go_names:
# 	go_names.update_one({'goName': doc['goName']},
# 		{"$set":doc}, upsert=True)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# list_of_names = []
# items = list(go_names.find())
# for each in items:
# 	list_of_names.append(each['goName'])
# pp.pprint(list_of_names)

my_list = []
access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)

# for name in list_of_names:
search_link= 'search?type=place&q=restaurants&center=37.8044,-122.2711&distance=10000&limit=100&fields=name,checkins,rating_count,single_line_address,category_list,location,price_range,overall_star_rating'
events = graph.request(search_link)
event_list= events['data']
my_list.append(event_list)


restaurants= []
this_list = my_list[0]

for item in this_list:
	# pp.pprint(item['name'])
	new = {}
	new['name']= item['name']
	new['single_line_address']= item['single_line_address']
	new['checkins']= [{
		'checkins': item['checkins'],
		'query_date': str(now)
	}]
	new['rating_count']= [{
		'rating_count': item['rating_count'],
		'query_date': str(now)
		}
	]
	new['overall_star_rating'] = [{
		'star_rating': item.get('overall_star_rating'),
		'query_date': str(now)
	}]
	new['category_list'] = item['category_list']
	new['location'] = {
		'latitude': item['location']['latitude'],
		'longitude': item['location']['longitude']
	}
	new['price_range'] = item.get('price_range')
	new['fbId']= item['id']
	restaurants.append(new)

fb_restaurants = db.Fbrestaurants
for item in restaurants:
	fb_restaurants.update_one({'fbId': item['fbId']},
		{"$set":item}, upsert=True)

print('done')
