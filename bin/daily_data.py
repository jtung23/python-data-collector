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

restaurants = list(all_restaurants.find())

yelp_ids = []
for each in restaurants:
	yelp_ids.append(each['yelpId'])

fb_ids = []

# from IPython import embed; embed()

for each in restaurants:
	fb_ids.append(each['fbId'])

# Yelp update
updated_list = []
for each in yelp_ids:
	yelp_id = each
	r = requests.get(
		'https://api.yelp.com/v3/businesses/' + yelp_id, 
		headers={
			"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'
			}).json()
	all_restaurants.find_one_and_update({
		'yelpId': r['id']
		},
		{'$push': {
			'reviews': {
				'review_count': r['review_count'],
				'query_date': str(now)
			}
		}}
		# '$set': {'rating': value['rating']}
	)

print('yelp done')

# Facebook update
for each in fb_ids:
	fb_id = each
	search_link= fb_id + '?fields=name,rating_count,checkins'
	restaurants = graph.request(search_link)
	all_restaurants.find_one_and_update({
		'fbId': restaurants['id']
	},
	{
		'$push': {
			'rating_count': {
				'rating_count': restaurants['rating_count'],
				'query_date': str(now)
			},
			'checkins': {
				'checkins': restaurants['checkins'],
				'query_date': str(now)
			}
		}
	})

print('fb done')