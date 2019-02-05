import os
import pygame
from pygame.locals import *
import pygame.gfxdraw
import math
import cairo
import numpy

from speedometer import *
from sideview import *
from weather import *
from graph import *
from music import *
from obd2 import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

task = 0
task_current = 0
surface_x = 0

# Draw 
color_back = (20,20,20)
color_text = (220,220,220)
color_speedo_back = (22,22,22)
color_speedo = (63,155,217)

# Draw once
surface_fuelusing = draw_graph()

# Running endless
clock = pygame.time.Clock()
running = True
mousehold = False
mousehold_x = 0
info = 0
o = 0
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

		if event.type == pygame.MOUSEBUTTONUP:
			if mousehold == True:
				if surface_x < -(task * screen_width) - 128:
					task += 1
				elif surface_x > -(task * screen_width) + 128:
					task -= 1
				mousehold = False

		if event.type == pygame.MOUSEMOTION:
			if mousehold == True:
				mouse = pygame.mouse.get_pos()
				surface_x = mouse[0] + surfacehold_x

		event_music(task_current, event)

	# Smooth page select
	if (mousehold == False):
		if(int(surface_x) < - task * screen_width):
			surface_x += (math.fabs(surface_x + (task * screen_width)) * 0.2)
		if(int(surface_x) > - task * screen_width):
			surface_x -= (math.fabs(surface_x + (task * screen_width)) * 0.2)
		if(math.fabs(surface_x + (task * screen_width)) < 2):
			task_current = task

	# Draw hud
	screen.fill(color_back)

	surface_speedometer = draw_speedometer()
	surface_sideview = draw_sideview()
	surface_weather = draw_weather()
	surface_music = draw_music()

	screen.blit(surface_speedometer, (surface_x + (screen_width * 0),0))
	screen.blit(surface_fuelusing, (surface_x + (screen_width * 1),0))
	screen.blit(surface_sideview, (surface_x + (screen_width * 2),0))
	screen.blit(surface_weather, (surface_x + (screen_width * 3),0))
	screen.blit(surface_music, (surface_x + (screen_width * 4),0))

	pygame.display.update()
	clock.tick(60)

obdconn.unwatch_all()
obdconn.close()
pygame.quit()