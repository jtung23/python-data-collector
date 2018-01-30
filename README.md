# Tregg Data Collection Scripts

## Purpose
These files were created for the initial data collection and contain automated scripts used daily by [Tregg](https://github.com/D-J-Trending/trending-restaurants) to analyze what restaurants are trending.

Node was initially used but a large api call to Yelp and Facebook repeatedly returned errors due to the amount of async calls being made in the for loop.
Switched over to Python due to the ability of finishing a task before moving on to the next, thus avoiding the error entirely.

## Links
>[Git Repo](https://github.com/D-J-Trending/trending-restaurants)

>[Site](https://tregg.herokuapp.com/)


## Code

### daily_data.py
Used to update certain fields in the mLab database used by Trending Restaurants as well as add new restaurants if the user added new restaurants.
There are two databases, `all_restaurants` and `all_ids`. The first contains all of the collected data and restaurant information, the second contains all of the current ids and any that get added to the database from the user.

- Updating existing restaurants Facebook information. Using pythons `get()` to return null if the field does not exist.

```python
# Facebook update
for each in fb_ids:
	fb_id = each
	search_link= fb_id + '?fields=name,rating_count,checkins,overall_star_rating'
	fb_res = graph.request(search_link)
	all_restaurants.find_one_and_update({
		'fbId': fb_res['id']
	},
	{
		'$push': {
			'rating_count': {
				'rating_count': fb_res['rating_count'],
				'query_date': str(now)
			},
			'checkins': {
				'checkins': fb_res['checkins'],
				'query_date': str(now)
			},
		},
		'$set': {
			'star_rating': {
				'overall_star_rating': fb_res.get('overall_star_rating'),
				'query_date': str(now)
			}
		}
	})
```

- Adding a new restaurant to `all_restaurants` collection from `all_ids` collection if it does not exist using dictionary comprehension and conditional statements.

```python
# gets array of ids that need to be added to collection
missing_id = []
all_ids_cut = {x['yelpId']: x for x in all_restaurant_ids}
for item in new_ids:
    if item['yelpId'] not in all_ids_cut:
        missing_id.append(item)
    else:
        pass  # whatever
final_missing = []
# inputs into array if no match
for ea in missing_id:
	if not any(d['yelpId'] == ea['yelpId'] for d in final_missing):
		final_missing.append(ea)
```

### do_math.py
Used daily to calculate the trending score and rank using our propriety algorithm. This data is inserted into the appropriate document for usage on the front-end to show which restaurants are the trendiest.

-Utilizing list comprehension to efficiently filter and modify arrays. Then sorting and establishing a rank or lack of rank for each document in the collection.
```python
# replace all scores with 'None' with 0.0 to sort
none_list = [x for x in doobie if len(x['checkins']) <= 10]

replaced_none = [x for x in doobie if x['score'] != None]
# have array of scores, now sort by score
sorted_score_list = sorted(replaced_none , key=itemgetter('score'), reverse=True)

for i, scores in enumerate(sorted_score_list):
	scores['new_rank'] = i + 1

for nones in none_list:
	nones['rank'] = 'Not Enough Data'
```

