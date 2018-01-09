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
restaurants = list(all_restaurants.find())
test = list(test_collection.find())
# all_links = []
# for item in restaurants:
# 	place_id = item['fbId']
# 	search_link= place_id + '?fields=name,link'
# 	links = graph.request(search_link)
# 	all_links.append({
# 		'fbId': item['fbId'],
# 		'name': links['name'],
# 		'link': links['link']
# 	})
# pp.pprint(all_links)
# print(len(all_links))

for these in restaurants:
	test_collection.update_one({'fbId': these['fbId']},
		{'$set': these}, upsert=True
	)
pp.pprint(test)
from IPython import embed; embed()
