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

access_token= 'EAAG0XCqokvMBADXjKrYtgQtp6E1PCWuUOXJ1ZBCOs1rGwp4tBOzJR0IcndbZAH83g3PGhZASgNmuvt0YEPafpCMzX6civGEQOHg8DWIgDILaniCbmnyTwmyDHbVbR53OEEbLT8c9AZBKy01THwgLCGTl3xZB1Xc8XpV5lNDsTogZDZD'
graph = facebook.GraphAPI(access_token=access_token, 
	version = 2.7)

fb_restaurants = db.Fbrestaurants

fbrestaurants = list(fb_restaurants.find())

locations = []
new = []
new_data = []

list_fb = []
for each in fbrestaurants:
	name = each['name']
	fbId = each['fbId']
# 	lat = each['location']['latitude']
# 	longitude = each['location']['longitude']

	list_fb.append({
		"name": name,
		"fbId": fbId,
# 		"lat": lat,
# 		"long": longitude
	})

for item in list_fb:
	place_id = item['fbId']
	search_link= place_id + '?fields=name,location'
	restaurants = graph.request(search_link)

	name = restaurants['name']
	street = restaurants['location']['street']
	city = restaurants['location']['city']
	state = restaurants['location']['state']
	# country = restaurants['location']['country'] 
	new.append({
		'name': name,
		'street': street,	
		'city': city,
		'state': state,
		'country': 'US',
		'fbId': place_id
		})

headers = []
for value in new:
	req = requests.get('https://api.yelp.com/v3/businesses/matches/best', 
		params= {'name': value['name'], 'address1': value['street'], 'city': value['city'], 'state': value['state'], 'country': value['country']},
		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
	firm = req.get('businesses', None)
	if firm == []:
		print('nothing')
	else:	
		print('appended')
		yelp_id = firm[0]['id']
		headers.append({
			'yelp_id': yelp_id,
			'fbId': value['fbId']
		})

final = []

for val in headers:

	r = requests.get('https://api.yelp.com/v3/businesses/' + val['yelp_id'], 
		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
	dat={}
	dat['name']= r['name']
	dat['yelpId']= r['id']
	dat['fbId']=val['fbId']
	dat['price'] = r.get('price')
	dat['rating']= [{
		'rating': r['rating'],
		'query_date': str(now)
	}]
	dat['reviews']= [{
		'review_count': r['review_count'],
		'query_date': str(now)
		}
	]
	dat['categories']= r['categories']
	dat['phone']= r['display_phone']
	dat['yelpURL']= r['url']
	dat['yelpImg']= r['image_url']
	dat['location']= {
		'address': r['location']['address1'],
		'city': r['location']['city'],
		'state': r['location']['state'],
		'country': r['location']['country']
	}
	final.append(dat)

pp.pprint(final)
# # from IPython import embed; embed()

all_restaurants = db.all_restaurants

for data in final:
	all_restaurants.update_one({'yelpId': data['yelpId']},
		{"$set":data}, upsert=True)
print(all_restaurants.count())