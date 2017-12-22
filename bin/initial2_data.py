# Logic:
# find fbid from fbrestaurants
# search through yelp db with fb information
# pull from yelp db and plug into object
# 
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

client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g

all_restaurants = db.AllRestaurants

# from IPython import embed; embed()

restaurants = list(all_restaurants.find())
pp.pprint(restaurants)
fb_list = []
for each in restaurants:
	data = {
		'fbId': each.get('fbId'),
		'name': each['name']
		# 'location': each['location']
	}
	fb_list.append(data)
pp.pprint(fb_list)
print(len(fb_list))

access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)

new_data = []
for item in fb_list:
	place_id = item['fbId']
	search_link= place_id + '?fields=name,rating_count,checkins,overall_star_rating'
	firms = graph.request(search_link)
	new_data.append(firms)

pp.pprint(new_data)
# from IPython import embed; embed()
for each in new_data:
	all_restaurants.find_one_and_update({
		'fbId': each['id']
	},
	{
		'$set': {
			'checkins': [{
				'checkins': each['checkins'],
				'query_date': str(now)
			}],
			'star_rating': [{
				'overall_star_rating': each.get('overall_star_rating'),
				'query_date': str(now)
			}],
			'rating_count': [{
				'rating_count': each['rating_count'],
				'query_date': str(now)
			}],
		}
	})

print('done')