# Display tools for figures

#############
## Imports ##
#############

import enum
from matplotlib import colors
from matplotlib import pyplot as plt
import numpy as np

###############
## Constants ##
###############

#############
## Classes ##
#############

class _Constants(enum.Enum):
	"""
	Parent abstract class for inheritage
	"""
	def __eq__(self, val):
		if not isinstance(val, str):
			raise TypeError()
		else:
			return self.value == val


class Projection(_Constants):
	"""
	Projection enumeration to access projection names.
	"""
	Cylindrical_Equidistant = "cyl"
	Mercator = "merc"
	Transverse_Mercator = "tmerc"
	Oblique_Mercator = "omerc"
	Miller_Cylindrical = "mill"
	Gall_Stereographic_Cylindrical = "gall"
	Cylindrical_Equal_Area = "cea"
	Lambert_Conformal = "lcc"
	Lambert_Azimuthal_Equal_Area = "laea"
	North_Polar_Lambert_Azimuthal = "nplaea"
	South_Polar_Lambert_Azimuthal = "splaea"
	Equidistant_Conic = "eqdc"
	Azimuthal_Equidistant = "aeqd"
	North_Polar_Azimuthal_Equidistant = "npaeqd"
	South_Polar_Azimuthal_Equidistant = "spaeqd"
	Albers_Equal_Area = "aea"
	Stereographic = "stere"
	North_Polar_Stereographic = "npstere"
	South_Polar_Stereographic = "spstere"
	Cassini_Soldner = "cass"
	Polyconic = "poly"
	Orthographic = "ortho"
	Geostationary = "geos"
	Near_Sided_Perspective = "nsper"
	Sinusoidal = "sinu"
	Mollweide = "moll"
	Hammer = "hammer"
	Robinson = "robin"
	Kavrayskiy_VII = "kav7"
	Eckert_IV = "eck4"
	Van_Der_Grinten = "vandg"
	McBryde_Thomas_Flat_Polar_Quartic = "mbtfpq"
	Gnomonic = "gnom"
	Rotated_Pole = "rotpole"

class MidpointNormalize(colors.Normalize):
	"""
	Useful object enbling to normalize colorbar with a chosen midpoint.
	"""
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)
	
	def __call__(self, value, clip=None):
		x, y = [self.vmin, self.midpoint, self.vmax], [0,0.5,1]
		return np.ma.masked_array(np.interp(value, x, y))

###############
## Functions ##
###############

def get_list_projections():
	"""
	Return a list of all available projections.
	"""
	return [f"{elt.value} ({elt.name})" for elt in Projection]

def get_cmap():
	"""
	Return list of available colormaps.
	"""
	return plt.colormaps()

def main():
	print(get_list_projections())

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)