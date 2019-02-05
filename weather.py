import os
import json
import cairo
import pygame
import requests
from pprint import pprint
from drawlib import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

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

# Get weather from api
weather = get_weather()

# Import weather images
weatherimage = {}
weatherfiles = os.listdir("weather/")

for file in weatherfiles:
    if file.endswith(".png"):
        weatherimage[file] = cairo.ImageSurface.create_from_png("weather/" + file)

print(weatherimage)

def draw_weather():

    # Init cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
    ctx = cairo.Context(surface)

    # If error message is empty
    if 'message' not in weather:
        x = 8
        y = 28

        ctx.set_font_size(24)
        ctx.set_source_rgb(1,1,1)
        draw_text(ctx, x, y + (30 * 0), 'Hely: ' + str(weather['name']))
        draw_text(ctx, x, y + (30 * 1), 'Hőmérséklet: ' + str(weather['main']['temp']) + '°')
        draw_text(ctx, x, y + (30 * 2), 'Szél: ' + str(weather['wind']['speed']) + ' meter/sec')

        for w in weather['weather']:
            draw_text(ctx, x, y + (30 * 3), w['description'])

            # Draw image
            if w['icon'] in weatherimage:
                ctx.set_source_surface(weatherimage[w['icon'] + '.png'], 4, 128) 
                ctx.paint()
    else:

        # Error message
        ctx.set_font_size(24)
        ctx.set_source_rgb(1,1,1)
        draw_text(ctx, 8, 28, str(weather['message']))

    # Convert to surface
    return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')