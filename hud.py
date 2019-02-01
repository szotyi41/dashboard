import pygame
from pygame.locals import *
import pygame.gfxdraw
import math
import cairo
import numpy
from drawlib import *

# Graph
import matplotlib as mpl
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
mpl.use("Agg")

# Weather
from weather import *

'''
	Időjárás
	Átlagfogyasztás
	Megtett út
	Megtenni kívánt út
	GPS
	Hatótáv
	Jelenlegi fogyasztás
	Üzemanyag mennyiség
	Üzemanyag típusa
	Üzemanyag ára
	Most tankoltam
	Megtett km mióta tankoltál
	Olajcsere
	Motor hömérséklet
	Ajtók nyitva
	Kamera
	Zenelejátszó
	Időmérés (Rendes + Negyedmérföld)
	Engine run time
	Guminyomás
	Throttlepos
'''

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

task = 0
task_current = 0

surface_speedometer = pygame.Surface(screen_size)
surface_fuelusing = pygame.Surface(screen_size)
surface_sideview = pygame.Surface(screen_size)
surface_weather = pygame.Surface(screen_size)
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

	screen.blit(surface_speedometer, (surface_x + (screen_width * 0),0))
	screen.blit(surface_fuelusing, (surface_x + (screen_width * 1),0))
	screen.blit(surface_sideview, (surface_x + (screen_width * 2),0))
	screen.blit(surface_weather, (surface_x + (screen_width * 3),0))

	pygame.display.update()

def draw_speedometer():

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	# Draw kmh
	x = int(screen_center[0] - (screen_center[0] / 2))
	y = int(screen_center[1])
	r = 120

	ctx.set_source_rgb(1,1,1)
	ctx.set_font_size(54)
	draw_text_center(ctx, x, y + 20, '20')
	ctx.set_font_size(28)
	draw_text_center(ctx, x, y + 48, 'kmh')

	ctx.set_line_width(6)
	ctx.set_source_rgb(0.12, 0.12, 0.12)
	ctx.arc(x, y, r, 0, 2 * math.pi)
	ctx.stroke()

	# Blue line
	r = 110
	start = 0.8 * math.pi
	end = (0.8 * math.pi) + (1.2 * math.pi)

	ctx.set_line_width(6)
	ctx.set_source_rgb(0.85,0.61,0.24)
	ctx.arc(x, y, r, start, end)
	ctx.stroke()

	# Draw rpm
	x = int(screen_center[0] + (screen_center[0] / 2))
	y = int(screen_center[1])
	r = 120

	ctx.set_source_rgb(1,1,1)
	ctx.set_font_size(54)
	draw_text_center(ctx, x, y + 20, '800')
	ctx.set_font_size(28)
	draw_text_center(ctx, x, y + 48, 'rpm')

	ctx.set_line_width(6)
	ctx.set_source_rgb(0.12,0.12,0.12)
	ctx.arc(x, y, r, 0, 2 * math.pi)
	ctx.stroke()

	# Blue line
	r = 110
	start = 0.8 * math.pi
	end = (0.8 * math.pi) + (1.2 * math.pi)

	ctx.set_line_width(6)
	ctx.set_source_rgb(0.85,0.61,0.24)
	ctx.arc(x, y, r, start, end)
	ctx.stroke()

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
	plt.plot(x, x, label="Consumption")
	plt.xlabel('Way (km)')
	plt.ylabel('Consumption (l/100km)')
	plt.title("Average consumption")
	plt.legend()

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()

	size = canvas.get_width_height()
	surf = pygame.image.fromstring(raw_data, size, "RGB")
	surface_fuelusing.blit(surf, (0,0))

def draw_sideview(ctx):

	# Import image
	image = pygame.image.load("golf.jpg")
	image = pygame.transform.scale(image, screen_size)
	imagerect = image.get_rect()

	# Draw image
	ctx.fill(color_back)
	ctx.blit(image, imagerect)
	pygame.display.update()

def draw_weather():

	# Init cairo
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
	ctx = cairo.Context(surface)

	# Get weather from api
	weather = get_weather()

	# If error message is empty
	if 'message' not in weather:
		# Draw
		x = 8
		y = 28

		ctx.set_font_size(24)
		ctx.set_source_rgb(1,1,1)
		draw_text(ctx, x, y + (30 * 0), 'Location: ' + str(weather['name']))
		draw_text(ctx, x, y + (30 * 1), 'Temp: ' + str(weather['main']['temp']) + '°')
		draw_text(ctx, x, y + (30 * 2), 'Windspeed: ' + str(weather['wind']['speed']) + ' meter/sec')

		for w in weather['weather']:
			draw_text(ctx, x, y + (30 * 3), w['description'])
	else:

		# Error message
		ctx.set_font_size(24)
		ctx.set_source_rgb(1,1,1)
		draw_text(ctx, 8, 28, str(weather['message']))

	# Convert to surface
	return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')

# Draw once
draw_graph(surface_fuelusing)
draw_sideview(surface_sideview)
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
			mouse = list(pygame.mouse.get_pos())
			surfacehold_x = surface_x - mouse[0]
			mousehold = True

		if event.type == pygame.MOUSEBUTTONUP:
			if surface_x < -task * screen_width:
				task += 1
			elif surface_x > -task * screen_height:
				task -= 1
			mousehold = False

		if event.type == pygame.MOUSEMOTION:
			if mousehold == True:
				mouse = list(pygame.mouse.get_pos())
				surface_x = mouse[0] + surfacehold_x

	# Smooth page select
	if (mousehold == False):
		if(int(surface_x) < - task * screen_width):
			surface_x += (math.fabs(surface_x + (task * screen_width)) * 0.2)
	
		if(int(surface_x) > - task * screen_width):
			surface_x -= (math.fabs(surface_x + (task * screen_width)) * 0.2)

	draw_hud()
	clock.tick(60)

pygame.quit()