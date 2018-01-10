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

access_token= 'EAAdISGCRkqMBABL06kxKZAQIdeGYOXi8BAoUoeqo22JzsJTKLNToOZATMorNQZB82ztrj0dCqqSUggHgUBXpQvRAK6lSi5PODzw0mIxDaT0Vaq1Mu2jQMj1kJDNbu8livWAkNnc4DFYN1OZBvMykelie2lZA4uUwZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)

all_restaurants = db.all_restaurants
test_collection = db.test_collection
restaurants = list(all_restaurants.find({'is_closed': False}))
test = list(all_restaurants.find({'is_closed': True}))
pp.pprint(len(restaurants))
pp.pprint(len(test))
all_links = []
# for item in restaurants:
# 	r = requests.get('https://api.yelp.com/v3/businesses/' + item['yelpId'], 
# 		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()

# 	place_id = item['fbId']
# 	search_link= place_id + '?fields=name,link'
# 	links = graph.request(search_link)
# 	all_links.append({
# 		'fbId': item['fbId'],
# 		'name': links['name'],
# 		'is_closed': r['is_closed'],
# 		'fbURL': links['link']
# 	})
# pp.pprint(all_links)
# # print(len(all_links))

# for these in all_links:
# 	all_restaurants.update_one({'fbId': these['fbId']},
# 		{'$set': {'fbURL': these['fbURL'], 'is_closed': these['is_closed']}}
# 	)
from IPython import embed; embed()
