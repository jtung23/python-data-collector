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

restaurants = (list(all_restaurants.find()))

# from IPython import embed; embed()
# 	pp.pprint(modified_checks)
# for each in restaurants:
# 	test.update_one({'yelpId': each['yelpId']},
# 		{"$set":each}, upsert=True)
# for each in restaurants:
# 	test.update_one({'yelpId': each['yelpId']},
# 	  { '$pull': { 'checkins': {'$elemMatch': {'query_date': '2017-12-27 16:45:10.762218' } } } }
# 	)

# for each in restaurants:
# 	test.update({'yelpId': each['yelpId']},
# 	  { '$pull': { 'checkins': {'$elemMatch': {'query_date': '2017-12-27 05:48:35.033732' } } } }
# 	)


# result = all_restaurants.find({
# 	'checkins': 
# })
# print(list(result))
# id_arr = []
# for the in restaurants:
# 	if (len(the['rating_count']) == 2):
# 		pp.pprint(the['yelpId'])
# 		id_arr.append(the['yelpId'])
# print(id_arr)

# for each in id_arr:
# 	result = all_restaurants.delete_one({'yelpId': each})
# 	print(result.deleted_count)
# 	print(all_restaurants.count())
# pp.pprint([each['name'] for each in restaurants if len(each['rating_count'][0][0]) == 1])
# for each in restaurants:
# 	test.update_one({'yelpId':each['yelpId']},
# 		{"$set":each}, upsert=True)
