# Figure main functionalities

#############
## Imports ##
#############

# Matplotlib imports
from mpl_toolkits.basemap import Basemap
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Other imports
import netCDF4 as nc
import numpy as np

# Custom imports
import display_tools

###############
## Constants ##
###############

#############
## Classes ##
#############

class Figure():
	"""
	Figure is an object containing data to plot and map options.
	It enables to easily draw a map with data on it.
	"""
	def __init__(self, figure : plt.Figure, ax : plt.Axes, dataset : nc.Dataset, map_options : dict, presets : dict):
		self.figure = figure
		self.ax = ax
		self.presets = presets
		self.map_options = map_options
		self.map_settings = self._get_map_settings()
		
		self.map = Basemap(ax=self.ax, **self.map_settings)
		self.map.drawmapboundary(fill_color='aqua')
		self.map.drawcoastlines()
		if self.map_options['countries']:
			self.map.drawcountries()
		if self.map_options['rivers']:
			self.map.drawrivers()
		
		# Extract longitude and latitude arrays (try 2 different name formats)
		try:
			self.lons = np.ma.getdata(dataset['lon'][:])
			self.lats = np.ma.getdata(dataset['lat'][:])
		except:
			self.lons = np.ma.getdata(dataset['longitude'][:])
			self.lats = np.ma.getdata(dataset['latitude'][:])

		self.data = self._retrieve_data_from_dataset(dataset)
		
		self.transform_data()

	def _get_map_settings(self):
		"""
		Return the basemap kwargs from global map options.
		"""
		settings = self.presets[self.map_options['preset']]['args'].copy()
		settings['resolution'] = self.map_options['resolution']
		return settings

	def _retrieve_data_from_dataset(self, dataset : nc.Dataset):
		"""
		Extract data from the dataset and process it.
		"""
		if self.map_options['pl_index'] is not None:
			data = dataset[self.map_options['variable']][self.map_options['time_index'], self.map_options['pl_index'], :, :]
		else:
			data = dataset[self.map_options['variable']][self.map_options['time_index'], :, :]
		data = data*self.map_options['coef']+self.map_options['offset']
		return data

	def transform_data(self):
		"""
		Transform the data.
		"""
		lon_offset = self.map_options['lon_offset']
		self.lons = self.lons+lon_offset
		temp = self.data[:, 0:720].copy()
		self.data[:, 0:720] = self.data[:, 720:1440].copy()
		self.data[:, 720:1440] = temp

	def adapt_coordinates(self):
		"""
		Adapt coordinates to the chosen projection.
		"""
		x, y = np.meshgrid(self.lons, self.lats)
		xx, yy = self.map(x, y)
		xx[~np.isfinite(xx)] =-180
		yy[~np.isfinite(yy)] = 0
		return xx, yy

	def plot_data(self):
		"""
		Plot data on the map.
		"""
		lon, lat = self.adapt_coordinates()

		if self.map_settings['projection'] == "ortho":
			self.data[lon>1e20] = np.nan
			self.data[lat>1e20] = np.nan
			self.data[lon<-1e20] = np.nan
			self.data[lat<-1e20] = np.nan

		if self.map_options['norm']:
			norm = display_tools.MidpointNormalize(
												   vmin=self.map_options['c_min'],
												   vmax=self.map_options['c_max'],
												   midpoint=self.map_options['midpoint']
												   )
		else:
			norm = None

		mesh = self.map.pcolormesh(lon, lat, self.data, cmap=self.map_options['cmap'], norm=norm)

		if self.map_options['colorbar']:
			divider = make_axes_locatable(self.ax)
			cax = divider.append_axes("right", size='3%', pad=0.1)
			plt.colorbar(mappable=mesh, ax=self.ax, cax=cax, orientation='vertical', extend='both')
		


###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)