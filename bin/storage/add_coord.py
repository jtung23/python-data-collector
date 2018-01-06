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
all_ids = db.all_ids

# gets data from all_ids. adds initial data
allids = list(all_ids.find())
restaurants = list(all_restaurants.find())

# pulls id from database then looks through facebook api to pull coords
list_coord = []
for item in restaurants:
	req = requests.get('https://api.yelp.com/v3/businesses/' + item['yelpId'], 
		# params= {'name': value['name'], 'address1': value['street'], 'city': value['city'], 'state': value['state'], 'country': value['country']},
		headers={"Authorization": 'Bearer Dt0X2kf0ef_hQ5Jc_5FNnxheSlXdFX1-svTZE6AJP0J4lBoVuMFRl66QgPFblxpMN-_AHN9OL3mek81qVap7DEtTMK2MrXxXpTxV31SVTbe-qajxmCEGj_nHwuEuWnYx'}).json()
	list_coord.append({
		'coordinates': req['coordinates'],
		'yelpId': req['id']
	})

pp.pprint(list_coord)

for each in list_coord:
	all_restaurants.update_one({'yelpId': each['yelpId']},
		{"$set": {'coordinates': each['coordinates']}})
from IPython import embed; embed()
