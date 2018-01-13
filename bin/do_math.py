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
from operator import itemgetter, attrgetter, methodcaller

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

all_restaurants = db.all_restaurants
test_collection = db.test_collection
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

def find_velocity(perc_list, second, third):
	# reverses percentage list
	rev_checkins = perc_list[::-1]
	# gets last 7 days sum
	recent_sum = sum_list(rev_checkins, None, second)
	# gets days 7 to 14 sum
	previous_sum = sum_list(rev_checkins, second, third)
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

	checkin_vel7 = find_velocity(checkin_perc, 7, 14)
	rating_vel7 = find_velocity(rating_perc, 7, 14)
	review_vel7 = find_velocity(review_perc, 7, 14)

	checkin_vel14 = find_velocity(checkin_perc, 14, 28)
	rating_vel14 = find_velocity(rating_perc, 14, 28)
	review_vel14 = find_velocity(review_perc, 14, 28)

	score = {
		'trending_score': {
			'7day': {
				'checkins': checkin_vel7,
				'rating_count': rating_vel7,
				'review_count': review_vel7
			},
			'14day': {
				'checkins': checkin_vel14,
				'rating_count': rating_vel14,
				'review_count': review_vel14
			},
			'updated_on': str(now)
		}

	}

	all_restaurants.update_one({'yelpId': this['yelpId']},
		{"$set":score})
	
print('score updated')

new_restaurants = list(all_restaurants.find())
pp.pprint(new_restaurants)
doobie = []
for bam in new_restaurants:
	print(bam.get('new_rank'))
	doobie.append({
		'yelpId': bam['yelpId'],
		'rank': bam.get('new_rank'),
		'checkins': bam['checkins'],
		'score': bam['trending_score']['7day']['checkins']
	})

# replace all scores with 'None' with 0.0 to sort
none_list = [x for x in doobie if len(x['checkins']) <= 10]

replaced_none = [x for x in doobie if x['score'] != None]
# have array of scores, now sort by score
sorted_score_list = sorted(replaced_none , key=itemgetter('score'), reverse=True)

for i, scores in enumerate(sorted_score_list):
	scores['new_rank'] = i + 1

for nones in none_list:
	nones['rank'] = 'Not Enough Data'

for final in sorted_score_list:
	all_restaurants.update_one({'yelpId': final['yelpId']},
		{"$set": {
			'previous_rank': final['rank'],
			'new_rank': final['new_rank']
		}
	})

for fin in none_list:
	all_restaurants.update_one({'yelpId': fin['yelpId']},
		{"$set": {
			'previous_rank': fin['rank'],
			'new_rank': fin['rank']
		}
	})
print('do math completed')