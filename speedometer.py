import cairo
from drawlib import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

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