import cairo
import pygame
from drawlib import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

# Import image
trip_km = 0
trip_h = 0
carimg = Image.open("golf.png")
carimage = pil2cairo(carimg, screen_width, screen_height)

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