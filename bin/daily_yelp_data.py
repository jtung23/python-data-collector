#!/usr/bin/env python

import json
import requests

import pymongo
from pymongo import MongoClient

import datetime
now = datetime.datetime.utcnow()

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

# Updates yelpId database based on id_arrays.json
# jsondata = json.load(open('/app/bin/id_arrays.json'))

# yelp_ids = jsondata['yelpArrIds']

yelpIds = db.yelpIds
# for doc in yelp_ids:
# 	yelpIds.update_one({'yelpId': doc['yelpId']},
# 		{"$set":doc}, upsert=True)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

items = list(yelpIds.find())

# # insert my_list into the collection
yelp_restaurants = db.yelprestaurants

# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
updated_list = []
# # # for looping through ids and returning new rating and review count
for val in items:
	yelp_id = val['yelpId']
	r = requests.get('https://api.yelp.com/v3/businesses/' + yelp_id, 
		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
	
	data={}

	data['yelpId']= r['id']
	data['rating']= r['rating']
	data['reviews']= {
		'review_count': r['review_count'],
		'query_date': str(now)
		}
	updated_list.append(data)
# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# # to update rating and reviews
for value in updated_list:
	yelp_restaurants.find_one_and_update({
		'yelpId': value['yelpId']
		},
		{
		'$push': {
			'reviews': value['reviews']
		}
		# '$set': {'rating': value['rating']}
		}
	)
# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

print('done')
