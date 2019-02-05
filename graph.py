import pygame
import matplotlib as mpl
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pylab
import numpy
mpl.use("Agg")

def draw_graph():

	color_back_fig = (20/255,20/255,20/255)

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
	return pygame.image.frombuffer(renderer.tostring_rgb(), size, "RGB")
	