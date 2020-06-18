# NC datasets tools extension

#############
## Imports ##
#############

import netCDF4 as nc

###############
## Constants ##
###############

#############
## Classes ##
#############

###############
## Functions ##
###############

def open_dataset(full_path : str):
	"""
	Open dataset using full path to the file.
	"""
	try:
		ds = nc.Dataset(full_path)
	except Exception as e:
		raise e
	return ds

def get_meta(ds : nc.Dataset):
	"""
	Return a ditionary with useful information on the dataset.
	Metadata are oraganised as follow:
	{
		'var_name': {
			'dimensions': (..., ),
			'shape': (..., ),
			'attributes': {
				'attr': '...'
			}
		}
	}
	"""
	meta = {}
	for var_name in ds.variables.keys():
		temp_dict = {}
		temp_dict['dimensions'] = ds[var_name].dimensions
		temp_dict['shape'] = ds[var_name].shape
		attr_dict = {}
		for attr in ds[var_name].ncattrs():
			attr_dict[attr] = ds[var_name].getncattr(attr)
		temp_dict['attributes'] = attr_dict
		meta[var_name] = temp_dict
	return meta

def retrieve_meta(full_path : str):
	"""
	Create a temporary dataset and retrieve only metadata.
	"""
	ds = open_dataset(full_path)
	return get_meta(ds)

def is_pressure_level(ds : nc.Dataset):
	"""
	Return True if given dataset has pressure levels.
	"""
	return 'level' in ds.dimensions

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)