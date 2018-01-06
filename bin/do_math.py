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
def sum_list(arr,first, last):
	sum = 0
	for x in arr[first:last]:
		int_x = float(x)
		sum += int_x
	return sum

def seperate_count(seq, filter):
	return [i[filter] for i in seq if i[filter]]

def percent_change(diff, totals):
	# divide diff[i] by totals[i]
	perc_change_list = []
	for i,each in enumerate(diff):
		percent = each/totals[i]
		perc_change_list.append(format(percent, '.6f'))
	return perc_change_list

def difference(arr):
	# seperates count into array
	checkins = seperate_count(arr['checkins'], 'checkins')
	ratings = seperate_count(arr['rating_count'], 'rating_count')
	reviews = seperate_count(arr['reviews'], 'review_count')

	# finds difference
	checkins_diff = list(numpy.diff(checkins))
	ratings_diff = list(numpy.diff(ratings))
	reviews_diff = list(numpy.diff(reviews))

	# finds %change, diff / total
	checkins_percent = percent_change(checkins_diff, checkins)
	ratings_percent = percent_change(ratings_diff, ratings)
	reviews_percent = percent_change(reviews_diff, reviews)
	data = {
		'fbId': arr['fbId'],
		'yelpId': arr['yelpId'],
		'checkins': {
			'difference': checkins_diff,
			'percent_change': checkins_percent
		},
		'rating_count': {
			'difference': ratings_diff,
			'percent_change': ratings_percent
		},
		'reviews': {
			'difference': reviews_diff,
			'percent_change': reviews_percent
		}
	}
	return data

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
	obj_diff = difference(data)
	diff_data.append(obj_diff)

# add last 7 percentchanges together, then
# weeklychange = recent 7 - previous 7
# total = weeklychange / previous7sum
# checkins total, ratings total, reviews total

def find_velocity(perc_list):
	# reverses percentage list
	rev_checkins = perc_list[::-1]
	# gets last 7 days sum
	recent_sum = sum_list(rev_checkins, None, 7)
	# gets days 7 to 14 sum
	previous_sum = sum_list(rev_checkins, 7, 14)
	weekly_change = recent_sum - previous_sum

	if weekly_change == 0.0 or previous_sum == 0.0:
		velocity = None
	else:
		velocity = weekly_change/previous_sum
	return velocity

for this in diff_data:

	checkin_perc = this['checkins']['percent_change']
	rating_perc = this['rating_count']['percent_change']
	review_perc = this['reviews']['percent_change']

	checkin_vel = find_velocity(checkin_perc)
	rating_vel = find_velocity(rating_perc)
	review_vel = find_velocity(review_perc)

	score = {
		'yelpId': this['yelpId'],
		'7day': {
			'checkins': checkin_vel,
			'rating_count': rating_vel,
			'review_count': review_vel
		}
	}
	pp.pprint(score)


# end product:
# score: {
# 	7day: {
# 		'checkins':
# 		'review_count':
# 		'rating_count':
#	}
# }
from IPython import embed; embed()



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