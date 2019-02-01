from pprint import pprint
import json
import requests

#https://openweathermap.org/weather-conditions

city_id = 3054643
url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&APPID=9d7c3c613f7362eca3f5c988f71e9d87'.format(city_id)

req_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'openweathermap.org',
    'Referer': 'https://openweathermap.org/city/2743477',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def get_weather():
	s = requests.Session()
	try:
		r = s.get(url, headers=req_headers)
	except requests.exceptions.RequestException as e:
		return json.loads('{"message":"Cannot connect to server"}')

	return json.loads(r.text)