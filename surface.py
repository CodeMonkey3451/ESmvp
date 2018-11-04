import logging
import numpy as np
import math


class Surface(object):
	"""Defining a surface in a 2D plane."""
	N_COORDS = 0 # Number of coordinates needed to uniquly define the surface

	def __init__(self, coordinates = [], **kwargs):
		"""coordinates need to be of the form: [x1, y1, x2, y2, ... , xn, yn]"""
		self.area = None
		self.coords = []
		self.setCoords(coordinates) # 2D np.array defining the shape


	def setCoords(self, coordinates):
		"""Set self.coords as np.array."""
		if len(coordinates) != self.N_COORDS:
			logging.warning('Could not set coordinates for {0} object. {1} coordinates \
				([x1, y1, x2, y2, ... , xn, yn]) needed.'.format(self.__class__.__name__, self.N_COORDS/2))
			return

		self.coords = np.array([])
		for i in range(0, len(coordinates)):
			self.coords = np.append(self.coords, coordinates[i])
		self.coords = self.coords.reshape(int((i+1)/2), 2)

		self.area = self.calcArea() # After the coordinates have been changed recalculate area


	def calcArea(self):
		"""Calculate area of the surface"""
		pass


	def getArea(self):
		"""Return area of the shape."""
		return self.area


class Polygon(Surface):
	"""Defining a surface as a polygon."""
	N_COORDS = 0 # Number of coordinates needed to uniquly define the surface

	def __init__(self, coordinates = [], **kwargs):
		self.area = None
		self.coords = None
		self.corners = None
		self.setCoords(coordinates) # 2D np.array defining the shape


	def setCoords(self, coordinates):
		"""Set self.coords as np.array."""
		if len(coordinates) != self.N_COORDS:
			logging.warning('Could not set coordinates for {0} object. {1} coordinates \
				([x1, y1, x2, y2, ... , xn, yn]) needed.'.format(self.__class__.__name__, self.N_COORDS/2))
			return

		self.coords = np.array([])
		for i in range(0, len(coordinates)):
			self.coords = np.append(self.coords, coordinates[i])
		self.coords = self.coords.reshape(int((i+1)/2), 2)

		self.setCorners() # After the coordinates have been changed set corners and recalculate area
		self.calcArea()


	def setCorners(self):
		"""Set coordinates of corners defining the polygon."""
		pass


class Rectangle(Polygon):
	"""Rectangle shape"""
	N_COORDS = 6 # Number of coordinates needed to uniquly define the surface

	def setCorners(self):
		"""Coordinates of the corners for a rectange."""
		P4 = self.coords[0,:] + self.coords[2,:] - self.coords[1,:]
		self.corners = np.append(self.coords, [P4], axis=0)


	def calcArea(self):
		"""Calculate area of the rectangle"""
		a = math.sqrt(sum((self.coords[1,:]-self.coords[0,:])**2))
		b = math.sqrt(sum((self.coords[2,:]-self.coords[1,:])**2))
		self.area =  a * b
