# Logic:
# Objective - store fbId, yelpId,3 day, 7 day, 14 day, 28 day.
# 	define function that does the math?
# Pull from AllRestaurant collection
# for each document
# 	store checkin, reviews, ratingcount in diff lists
# 	e.g. array: [{count: 35, query_date: 12/21/2017}, {count: 35, query_date: 12/21/2017}]
# 	do [index+1 - index]

import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.utcnow()

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

all_restaurants = db.all_restaurants
restaurants = list(all_restaurants.find())

pp.pprint(restaurants)
all_data = []
rating_count = []
reviews = []

# makes array of all checkins, rating count, and reviews 
for each in restaurants:
	obj = {
		'fbId': each['fbId'],
		'yelpId': each['yelpId'],
		'checkins': each['checkins'],
		'rating_count': each['rating_count'],
		'reviews': each['reviews']
	}
	all_data.append(obj)
# pp.pprint(all_data)

# for each in all_data:

# gets difference for last 3 days
# # finds difference
def difference (range, array):
	count = 0
	while count < range:
		pass
		for each in reversed(array):
			power = len(suffixes) - index
			print(index)
			pp.pprint(power)
			c

difference(3,all_data[0])