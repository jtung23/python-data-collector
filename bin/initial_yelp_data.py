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
# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

items = list(yelpIds.find())
my_list = []

# for looping through Ids and fresh inputting into db
for val in items:
	yelp_id = val['yelpId']
	r = requests.get('https://api.yelp.com/v3/businesses/' + yelp_id, 
		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
	
	data={}
	data['name']= r['name']
	data['yelpId']= r['id']
	data['price'] = r.get('price')
	data['rating']= [{
		'rating': r['rating'],
		'query_date': str(now)
	}]
	data['reviews']= [{
		'review_count': r['review_count'],
		'query_date': str(now)
		}
	]
	data['categories']= r['categories']
	data['phone']= r['display_phone']
	data['yelpURL']= r['url']
	my_list.append(data)

# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# # insert my_list into the collection
yelp_restaurants = db.yelprestaurants
# # 
# # To insert the array of new restaurants
for data in my_list:
	yelp_restaurants.update_one({'yelpId': data['yelpId']},
		{"$set":data}, upsert=True)
print(yelp_restaurants.count())

print('done')
