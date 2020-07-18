# desc

#############
## Imports ##
#############

# matplotlib imports
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

# Other imports
import os
import json

###############
## Constants ##
###############

IMAGES_PATH = "ressources\\images\\maps\\"
PRESETS_FILE = "utils\\figure\\map_presets.json"

#############
## Classes ##
#############

###############
## Functions ##
###############

def preset_formatter(filename : str, description : str, args : dict):
	"""
	Format information, load the presets file and add them.
	"""
	with open(PRESETS_FILE, 'r') as foo:
		map_presets = json.load(foo)
		foo.close()
	
	preset_name = filename.split(".")[0]
	temp_dict = {}
	temp_dict["description"] = description
	temp_dict["args"] = args
	temp_dict["filename"] = filename
	map_presets[preset_name] = temp_dict
	
	with open(PRESETS_FILE, 'w') as foo:
		json.dump(map_presets, foo, indent=4)
		foo.close()

def main():
	"""
	This function needs to be modified in order to generate the different previews.
	An idea should be to include parts of this code to create custom presets.
	"""
	## ARGUMENTS TO BE CHANGED BELOW THIS LINE ##
	filename = "sps.png"
	description = "South Polar stereographic projection." # Description to add to the preset
	args = {
			"projection": 'spstere',
			"boundinglat": -15,
			"lon_0": 0
			}
	## ARGUMENTS TO BE CHANGED ABOVE THIS LINE ##

	# Map creation
	m = Basemap(resolution='i', **args)
	m.drawcoastlines()
	m.fillcontinents()
	# Format uniformisation
	plt.tight_layout()
	# Save figure as a png file.
	plt.savefig(os.path.join(IMAGES_PATH, filename))
	preset_formatter(filename, description, args)

if __name__ == '__main__':
	main()
else:
	raise Exception(f"File {__file__} cannot be imported as a module.")