import logging
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

import surface

class Plotter(object):
	"""Plotting class"""

	def __init__(self):
		self.farmland = [] # Patches collection array
		self.beeland = []


	def getColors(self, landtype):
		"""Get Colors depending on land type."""
		edgecolor = 'black'
		if landtype == 'farmland':
			facecolor = 'peru'
		elif landtype == 'beeland':
			facecolor = 'green'
		else:
			"""Set unknown area types to gray"""
			facecolor = 'gray'
		return facecolor, edgecolor


	def addArea(self, land):
		"""Add the area of a Surface object to patches."""

		if issubclass(land.surf.__class__, surface.Polygon):
			obj = Polygon(land.surf.corners, True)
		else:
			logging.warning('Surface object type unknown. Could not add to area to plot.')
			return

		if land.landtype == 'farmland':
			self.farmland.append(obj)
		elif land.landtype == 'beeland':
			self.beeland.append(obj)


	def getAxisranges(self):
		"""Get x- and y-axis ranges."""
		# TODO !
		xmin = 0
		xmax = 10
		ymin = 0
		ymax = 10
		return xmin, xmax, ymin, ymax


	def draw(self):
		"""Draw all objects."""
		xmin, xmax, ymin, ymax = self.getAxisranges()

		fig, ax = plt.subplots()

		fcolor, ecolor = self.getColors('farmland')
		farms = PatchCollection(self.farmland, facecolor=fcolor, edgecolor=ecolor)
		ax.add_collection(farms)
		fcolor, ecolor = self.getColors('beeland')
		bees = PatchCollection(self.beeland, facecolor=fcolor, edgecolor=ecolor)
		ax.add_collection(bees)

		ax.set_xlim([xmin,xmax])
		ax.set_ylim([ymin,ymax])
		#fig.colorbar(p, ax=ax)

		plt.show()
