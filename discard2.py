import base64
import pandas as pd
import requests

#extracting hashtags from given JSON file
def get_hashtags(user):
	hashtag1 = []

	hashtag1.extend([item["text"] for item in user["entities"]["hashtags"]])
	if "retweeted_status" in user:
		hashtag1.extend([item["text"] for item in user["retweeted_status"]["entities"]["hashtags"]])
	return list(set(hashtag1))

#extracting user mentions from the given JSON file
def get_user_mentions(user):
	user_mentions = []

	user_mentions.extend([item["screen_name"] for item in user["entities"]["user_mentions"]])
	if "retweeted_status" in user:
		user_mentions.extend([item["screen_name"] for item in user["retweeted_status"]["entities"]["user_mentions"]])
	return list(set(user_mentions))

#'expanded_url'
def get_mentioned_urls(user):
	urls = []
	if "media" not in user["entities"]:
		return urls
	urls.extend([item["expanded_url"] for item in user["entities"]["media"]])
	if "retweeted_status" in user:
		urls.extend([item["expanded_url"] for item in user["retweeted_status"]["entities"]["media"]])
	return list(set(urls))

#getting date format from date
def get_date_format(date):
	date = date.split()
	date = date[1:3]+date[-1:]
	#print("date : " + str(date))
	return "-".join(date)

#getting time format from time
def get_time_format(time):
	time = time.split()
	#print("time : " + time[3])
	return time[3]

#defining a class
class Twitter():
	token = "-1"
	base_url = 'https://api.twitter.com/'
	def __init__(self,client_key = "",client_secret = ""):
		self.client_key = '6AkVKj6pXLrnZZvTVNQBYHO3E'#your client key
		self.client_secret = 'G4OcrNI3A2H7Hb192X3crBilJPfSoCrSdQvNjCgy0RDXSlgENY'#your secret key
	def set_urls(self):

		auth_url = '{}oauth2/token'.format(self.base_url)
		return auth_url
	def b64_encoded_key(self):
		key_secret = '{}:{}'.format(self.client_key, self.client_secret).encode('ascii')
		b64_encoded_key = base64.b64encode(key_secret)
		b64_encoded_key = b64_encoded_key.decode('ascii')
		return b64_encoded_key
	def auth_headers(self):
		auth_headers = {
    'Authorization': 'Basic {}'.format(self.b64_encoded_key()),\
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'\
	}
		return auth_headers
	def auth_data(self):
		auth_data = {
    'grant_type': 'client_credentials'\
	}
		return auth_data
	def get_token(self):
		auth_resp = requests.post(self.set_urls(), headers=self.auth_headers(), data=self.auth_data())
		try:
			auth_resp.json()
			access_token = auth_resp.json()['access_token']
			self.token = access_token
			return access_token
		except:
			return -1
	def search_city_woeid(self,lat=17,long=79):
		search_headers = {
    'Authorization': 'Bearer {}'.format(self.token)\
	}
		search_params = {
			'lat':lat,
			'long':long,
			#'accuracy':5000000,
			#'granularity':'neighborhood',
			#'query':'Toronto'
			#'q':q
			#'id':2295414
			}
		#2295414
		search_url = '{}1.1/trends/closest.json'.format(self.base_url)
		#1.1/trends/place.json?id=2295414
		#
		#1.1/trends/closest.json
		search_resp = requests.get(search_url, headers=search_headers, params=search_params)
		return search_resp
	def search_trends(self, id = 2295414):
		search_headers = {
    'Authorization': 'Bearer {}'.format(self.token)\
	}
		search_params = {
			#'lat':lat,
			#'long':long,
			#'accuracy':5000000,
			#'granularity':'neighborhood',
			#'query':'Toronto'
			#'q':q
			'id':id
			}
		#2295414
		search_url = '{}1.1/trends/place.json'.format(self.base_url)
		#1.1/trends/place.json?id=2295414
		#
		#1.1/trends/closest.json
		search_resp = requests.get(search_url, headers=search_headers, params=search_params)
		return search_resp

def get_trending_dict(search_key = "#Major"):
	item = Twitter()
	#print(item.get_token())
	import pprint
	cities_locations = {
	'hyderabad':{'lat':17.385,'long':78.486},
	'chennai':{'lat':13.082,'long':80.270},
	'delhi':{'lat':28.704,'long':77.102},
	'kolkata':{'lat':22.572,'long':88.363},
	'bengaluru':{'lat':12.9716,'long':77.594},
	'mumbai':{'lat':19.076,'long':72.877}
	}
	woeid = {}
	Tweet_Volume = {}

	for key,value in cities_locations.items():
		#print("------",key)
		woeid[key] = item.search_city_woeid(lat = value['lat'],long = value['long']).json()[0]['woeid']
		pprint.p#print(woeid[key])
		inp = item.search_trends(id = woeid[key]).json()
		Tweet_Volume.update({key:i['tweet_volume'] for i in inp[0]['trends'] if search_key in i['name']})
		pprint.p#print(inp)
		pprint.p#print(Tweet_Volume)

	#pprint.p#print(item.search_request().json())
	pprint.p#print(Tweet_Volume)
	return Tweet_Volume
	#f = open("yoyo.txt","w+")
	#f.write(str(item.search_request().json()))
