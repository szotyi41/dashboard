import os
import pygame
from pygame.locals import *
import pygame.gfxdraw
import math
import cairo
import numpy
import datetime

# Graph
import matplotlib as mpl
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
mpl.use("Agg")

from drawlib import *
from obd2lib import *
from weather import *
from music import *

trip_km = 0
trip_h = 0

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

task = 0
task_current = 0

surface_fuelusing = pygame.Surface(screen_size)
'''surface_speedometer = pygame.Surface(screen_size)
surface_sideview = pygame.Surface(screen_size)
surface_weather = pygame.Surface(screen_size)
surface_music = pygame.Surface(screen_size)'''
surface_x = 0

# Draw 
color_back = (20,20,20)
color_back_fig = (20/255,20/255,20/255)
color_text = (220,220,220)
color_speedo_back = (22,22,22)
color_speedo = (63,155,217)

def draw_hud():
	screen.fill(color_back)

	surface_speedometer = draw_speedometer()
	surface_sideview = draw_sideview()
	surface_music = draw_music()

	screen.blit(surface_speedometer, (surface_x + (screen_width * 0),0))
	screen.blit(surface_fuelusing, (surface_x + (screen_width * 1),0))
	screen.blit(surface_sideview, (surface_x + (screen_width * 2),0))
	screen.blit(surface_weather, (surface_x + (screen_width * 3),0))
	screen.blit(surface_music, (surface_x + (screen_width * 4),0))

	pygame.display.update()

# Draw music player
i = 0
mus = Music()
musiclist = mus.getlist()
mus.playfirst()

defaultimage = Image.open("default.png")
defaultcover = pil2cairo(defaultimage, 128, 128)


def draw_music():

	

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	i = 0
	for music in musiclist:
		
		if 'song' in music['data']['ID3TagV2']: 
			title = music['data']['ID3TagV2']['song'].encode(encoding='UTF-8',errors='ignore')
		else:
			title = music['filename']

		if 'cover' in music:
			cover = music['cover']
		else:
			cover = defaultcover

		x = i * 128
		y = 0

		ctx.save()
		ctx.fill()
		ctx.set_source_surface(cover, x, y)
		ctx.paint()
		ctx.stroke()
		ctx.restore()
		ctx.close_path()	

		ctx.save()
		ctx.set_font_size(24)
		ctx.set_source_rgb(1, 1, 1)
		draw_text_center(ctx,x+64,y+160, str(title))
		ctx.stroke()
		ctx.restore()
		ctx.close_path()	
		i += 1

	draw_button(ctx,32,256,128,128,"play")
	draw_text(ctx,160,256,"Time: "+str(mus.getposition()))

	return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')


# Draw speedometer
fuelicon = cairo.ImageSurface.create_from_png("icons/fuel.png")
tempicon = cairo.ImageSurface.create_from_png("icons/temp.png")

def draw_speedometer():

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	# Draw time
	x = int(screen_center[0])
	y = int(screen_center[1] - (screen_center[1] / 2))
	draw_time(ctx,x,y)

	# Draw kmh
	r = 120
	x = int(screen_center[0] - (screen_center[0] / 2))
	y = int(screen_center[1])
	draw_meter(ctx,x,y,r,'kmh',120,220)

	# Draw rpm
	r = 120
	x = int(screen_center[0] + (screen_center[0] / 2))
	y = int(screen_center[1])
	draw_meter(ctx,x,y,r,'rpm',4000,8000,True)

	# Draw fuellevel
	r = 32
	x = int(screen_center[0] - (screen_center[0] / 2) - 96)
	y = int(screen_height - 64)
	draw_level(ctx,x,y,r,fuelicon,20,100, True, True)

	# Draw enginetemp
	r = 32
	x = int(screen_center[0] + (screen_center[0] / 2) + 96)
	y = int(screen_height - 64)
	draw_level(ctx,x,y,r,tempicon,20,100, True)

	# Draw info
	x = int(screen_center[0])
	y = int(screen_height - 32)

	ctx.save()
	ctx.set_font_size(20)
	ctx.set_source_rgb(1, 1, 1)
	draw_text_center(ctx,x,y,'Hatótáv: 32 km')
	ctx.stroke()
	ctx.restore()
	ctx.close_path()	

	# Convert to surface
	return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')

def draw_graph(ctx):

	mpl.rcParams.update({
	    "lines.color": "white",
	    "patch.edgecolor": "white",
	    "text.color": "white",
	    "axes.facecolor": color_back_fig,
	    "axes.edgecolor": "lightgray",
	    "axes.labelcolor": "white",
	    "xtick.color": "white",
	    "ytick.color": "white",
	    "grid.color": "lightgray",
	    "figure.facecolor": color_back_fig,
	    "figure.edgecolor": "black",
	    "savefig.facecolor": "black",
	    "savefig.edgecolor": "black"
	})

	fig, ax = plt.subplots()
	x = numpy.linspace(0, 2, 10)
	plt.plot(x, x, label="Fogyasztás")
	plt.xlabel('Út (km)')
	plt.ylabel('Fogyasztás (l/100km)')
	plt.title("Átlagfogyasztás")
	plt.legend()

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()

	size = canvas.get_width_height()
	surf = pygame.image.frombuffer(renderer.tostring_rgb(), size, "RGB")
	surface_fuelusing.blit(surf, (0,0))

# Import image
carimage = cairo.ImageSurface.create_from_png("golf.png")

def draw_sideview():

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	# Draw image
	ctx.fill()
	ctx.scale(1,1)
	ctx.set_source_surface(carimage, -1, -1)
	ctx.paint()

	# Draw info
	ctx.set_font_size(24)
	ctx.set_source_rgb(1,1,1)
	draw_text(ctx, 32, 32 + (0 * 28), 'Megtett út: ' + str(trip_km) + ' km')
	draw_text(ctx, 32, 32 + (1 * 28), 'Motor futás idő: ' + str(trip_h))

	return pygame.image.frombuffer(surface.get_data(), screen_size, 'RGBA').convert()


# Import weather images
weatherimage = {}
weatherfiles = os.listdir("weather/")

for file in weatherfiles:
	if file.endswith(".png"):
		weatherimage[file] = cairo.ImageSurface.create_from_png("weather/" + file)

def draw_weather():

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	# Get weather from api
	weather = get_weather()

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
			ctx.set_source_surface(weatherimage[w['icon'] + '.png'], 4, 128) 
			ctx.paint()

	else:

		# Error message
		ctx.set_font_size(24)
		ctx.set_source_rgb(1,1,1)
		draw_text(ctx, 8, 28, str(weather['message']))

	# Convert to surface
	return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')

# Draw once
draw_graph(surface_fuelusing)
surface_weather = draw_weather()

# Running endless
clock = pygame.time.Clock()
running = True
mousehold = False
mousehold_x = 0
info = 0
while running:

	# Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    running = False

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
			if event.key == K_RIGHT:
				task += 1
			if event.key == K_LEFT:
				task -= 1

		# Change screens
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			surfacehold_x = surface_x - mouse[0]
			mousehold = True

			if task_current == 4:
				if hover(32,256,128,128):
					mus.playpause()

				i = 0
				for music in musiclist:
					if hover((i*128),0,(i*128)+110,128):
						mus.load(music['filename'])
					i+=1

		if event.type == pygame.MOUSEBUTTONUP:
			'''if surface_x < -task * screen_width:
				task += 1
			elif surface_x > -task * screen_height:
				task -= 1'''
			mousehold = False

		if event.type == pygame.MOUSEMOTION:
			if mousehold == True:
				mouse = pygame.mouse.get_pos()
				surface_x = mouse[0] + surfacehold_x

	# Smooth page select
	if (mousehold == False):
		if(int(surface_x) < - task * screen_width):
			surface_x += (math.fabs(surface_x + (task * screen_width)) * 0.2)
		if(int(surface_x) > - task * screen_width):
			surface_x -= (math.fabs(surface_x + (task * screen_width)) * 0.2)
		if(math.fabs(surface_x + (task * screen_width)) < 2):
			task_current = task

	draw_hud()
	clock.tick(60)

obdconn.unwatch_all()
obdconn.close()
pygame.quit()