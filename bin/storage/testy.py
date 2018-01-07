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

# # gets data from all_ids. adds initial data
# allids = list(all_ids.find())
restaurants = list(all_restaurants.find())

all_ids = []
for val in restaurants:
	all_ids.append({'yelpId': val['yelpId'], 'fbId': val['fbId']})
pp.pprint(all_ids)
# result = all_restaurants.find({'rating_count[0][0]': {
# 		'rating_count': {'$gte': 0}
# 	}
# })
# print(list(result))
# for the in restaurants:
# 	pp.pprint
# print(id_arr)

# for each in id_arr:
# 	result = all_restaurants.delete_one({'yelpId': each})
# 	print(result.deleted_count)
# 	print(all_restaurants.count())
# pp.pprint([each['name'] for each in restaurants if len(each['rating_count'][0][0]) == 1])
	
# print('start add new')
# # finds missing Id that needs to be added to all_restaurant
# yelp_ids = []
# all_ids = []
# for datum in allids:
# 	yelp_ids.append({'yelpId': datum['yelpId'], 'fbId': datum['fbId']})
# for val in restaurants:
# 	all_ids.append({'yelpId': val['yelpId'], 'fbId': val['fbId']})

# # gets array of ids that need to be added to collection
# missing_id =list(filter(lambda x: x not in all_ids, yelp_ids))

# headers = []

# for value in missing_id:
# 	place_id = value['fbId']
# 	search_link= place_id + '?fields=name,rating_count,checkins,overall_star_rating'
# 	firms = graph.request(search_link)

# 	r = requests.get('https://api.yelp.com/v3/businesses/' + value['yelpId'], 
# 		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
# 	dat={}
# 	dat['name']= r['name']
# 	dat['yelpId']= r['id']
# 	dat['fbId']=value['fbId']
# 	dat['price'] = r.get('price')
# 	dat['rating']= [{
# 		'rating': r['rating'],
# 		'query_date': str(now)
# 	}]
# 	dat['reviews']= [{
# 		'review_count': r['review_count'],
# 		'query_date': str(now)
# 		}
# 	]
# 	dat['checkins']= [
# 		{
# 			'checkins': firms['checkins'],
# 			'query_date': str(now)
# 		}
# 	]
# 	dat['star_rating']=[
# 		{
# 			'overall_star_rating': firms.get('overall_star_rating'),
# 			'query_date': str(now)
# 		}
# 	]
	# dat['rating_count']=[
	# 	{
	# 	'rating_count': firms['rating_count'],
	# 	'query_date': str(now)
	# 	}
	# ]
# 	dat['categories']= r['categories']
# 	dat['phone']= r['display_phone']
# 	dat['yelpURL']= r['url']
# 	dat['yelpImg']= r['image_url']
# 	dat['location']= {
# 		'address': r['location']['address1'],
# 		'city': r['location']['city'],
# 		'state': r['location']['state'],
# 		'country': r['location']['country']
# 	}
# 	headers.append(dat)

# pp.pprint(headers)

# for data in headers:
# 	all_restaurants.update_one({'yelpId': data['yelpId']},
# 		{"$set":data}, upsert=True)
# print('added new')
# print(all_restaurants.count())
# from IPython import embed; embed()
