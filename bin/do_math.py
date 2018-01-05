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
import statistics
import pymongo
from pymongo import MongoClient
import numpy
import pprint
pp = pprint.PrettyPrinter(indent=4)
from itertools import islice
import datetime
now = datetime.datetime.utcnow()

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

# returns the different values in list
# for each dict in list, find difference
# between value and value+1
# then save value+1 date
def seperate_count(seq, filter):
	pp.pprint(seq)
	return [i[filter] for i in seq if i[filter]]


def difference(arr):
	pp.pprint(arr)
	checkins = numpy.diff(seperate_count(arr['checkins'], 'checkins'))
	ratings = numpy.diff(seperate_count(arr['rating_count'], 'rating_count'))
	reviews = numpy.diff(seperate_count(arr['reviews'], 'review_count'))

	data = {
		'fbId': arr['fbId'],
		'yelpId': arr['yelpId'],
		'checkins': checkins,
		'rating_count': ratings,
		'reviews': reviews
	}
	return data
	
	# for each in all_data:
	# 	data = each[data_filter][::-1]
	# 	count = 0
	# 	stats = []

	# 	while count < numb:
	# 		stats.append(data[count][data_filter])
	# 		mean = statistics.mean(stats)
	# 		median = statistics.median(stats)
	# 		mode = statistics.mode(stats)
	# 		obj = {
	# 			numb + "_days": {
	# 				'mean':
	# 				'median':
	# 				'mode':
	# 			}	
	# 		}
	# 		count = count + 1

	# for i, value in enumerate(new_list['checkins']):
	# 	while i < 3:
	# 		print(i)
	# 		pp.pprint(value)
	# while count < numb:

all_restaurants = db.all_restaurants
restaurants = list(all_restaurants.find())

all_data = []

# makes array of all checkins, rating count, and reviews 
for each in restaurants:
	all_data.append({
		'fbId': each['fbId'],
		'yelpId': each['yelpId'],
		'checkins': each['checkins'],
		'rating_count': each['rating_count'],
		'reviews': each['reviews']
	})
diff_data = []

for data in all_data:
	pp.pprint(data)
	obj_diff = difference(data)
	diff_data.append(obj_diff)

pp.pprint(diff_data)