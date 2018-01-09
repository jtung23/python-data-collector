import json
import requests

import pymongo
from pymongo import MongoClient

import pprint
pp = pprint.PrettyPrinter(indent=4)

import datetime
now = datetime.datetime.utcnow()
import re
import facebook
regex=re.compile(".*(2018-01-09).*")
client = MongoClient('mongodb://admin:bootcamp123@ds159776.mlab.com:59776/heroku_vg8qr96g')
db = client.heroku_vg8qr96g
print(str(now))
access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)


all_restaurants = db.all_restaurants

allrest = (list(all_restaurants.find()))
# gets data from all_ids. adds initial data
# allids = list(all_ids.find())
restaurants = list(all_restaurants.find({
	'reviews': {
		'$elemMatch': {
			'query_date': {
				'$regex': '2018-01-09.*'
			}
		}
	}
	})
)

for each in restaurants:
	# each['checkins'] = [x for x in each['checkins'] if '2018-01-09 13:00:40.621865' not in x['query_date']]
	# each['rating_count'] = [x for x in each['rating_count'] if '2018-01-09 13:00:40.621865' not in x['query_date']]
	each['reviews'] = [x for x in each['reviews'] if '2018-01-09 13:00:40.621865' not in x['query_date']]
# pp.pprint(restaurants)

for each in restaurants:
	all_restaurants.update_one({'yelpId': each['yelpId']},
		{'$set': {'reviews': each['reviews']}}
	)
# pp.pprint(allrest)
from IPython import embed; embed()