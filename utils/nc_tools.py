# NC datasets tools extension

#############
## Imports ##
#############

import netCDF4 as nc
from datetime import date, timedelta

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

def is_pressure_level(ds : nc.Dataset = None, meta : dict = None):
	"""
	Return True if given dataset has pressure levels.
	"""
	if ds:
		return 'level' in ds.dimensions
	elif meta:
		return 'level' in meta.keys()
	else:
		raise Exception("ArgumentsError: You need to pass at least 1 argument.")

def _get_time(time, time_index : int):
	"""
	Return the time associated with the passed time index.
	"""
	offset_date = date(1900, 1, 1)
	hours_since = time[time_index]
	td = timedelta(days=int(hours_since/24))
	return (offset_date+td).isoformat()

def get_timesteps(ds : nc.Dataset):
	"""
	Return the list of all timesteps with format : '{index} : date'.
	"""
	time = ds['time'][:]
	timesteps = [f"{i} : "+_get_time(time, i) for i in range (len(time))]
	return timesteps

def get_variables(ds : nc.Dataset):
	"""
	Return the list of variables of a dataset.
	"""
	l_var = list(ds.variables.keys())
	l_index_to_pop = []
	for i in range (len(l_var)):
		if l_var[i] in ds.dimensions:
			l_index_to_pop.append(i)
	l_index_to_pop.sort(reverse=True)
	for index in l_index_to_pop:
		l_var.pop(index)
	return l_var

def get_pressure_levels(ds : nc.Dataset):
	"""
	Return list of available pressure levels for the dataset.
	"""
	if not is_pressure_level(ds):
		raise Exception("DatasetError: Unable to retrieve pressure levels from this dataset.")
	arr = ds['level'][:]
	levels = [f"{i} : "+str(arr[i]) for i in range ((arr.shape)[0])]
	return levels

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)