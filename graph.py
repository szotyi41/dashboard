import pygame
from pygame.locals import *
import pygame.gfxdraw
import math
import cairo
import numpy


# Graph
import matplotlib as mpl
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
import numpy
mpl.use("Agg")

window = (640, 480)
screen = pygame.display.set_mode(window, pygame.RESIZABLE)
screen_w = screen.get_width()
screen_h = screen.get_height()
center = [int(screen_w / 2), int(screen_h / 2)]

surface_fuelusing = pygame.Surface(window)
color_back_fig = (20/255,20/255,20/255)


	return surface_fuelusing