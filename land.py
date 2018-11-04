import logging
from surface import Rectangle

class Land():
	"""Basic class to define an area in a 2D plane with specific properties."""
	LANDTYPES = ['farmland', 'beeland']

	def __init__(self, landtype, surftype, coordinates):
		self.landtype = None # Type of land (e.g.: farmland, etc.)
		self.surf = None # Surface defining the land
		self.setLandtype(landtype)
		self.setSurface(surftype, coordinates)


	def setLandtype(self, landtype):
		"""Set the type of land."""
		if 	landtype in self.LANDTYPES:
			self.landtype = landtype
		else:
			logging.warning('Could not set landtype: {0}. Supported landtypes: {1}'.format(landtype, self.LANDTYPES))


	def setSurface(self, surftype, coordinates):
		"""Set surface depnding on type and coordinates."""
		if surftype == 'rect':
			self.surf = Rectangle(coordinates)
		else:
			logging.warning('Could not create Surface object of type {0}'.format(surftype))


	def getType(self):
		"""Return type of land."""
		return self.type


	def getArea(self):
		"""Return area of the land. [m^2]"""
		return self.surf.getArea()
