# Panels module

#############
## Imports ##
#############

# Paths fixing
import sys
if __name__ == '__main__':
	sys.path.append("features")

# GUI imports
import wx
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl

# Other imports
import netCDF4 as nc # Not used for its functions, only for typing

# Custom imports
from features import subpanels
import nc_tools

###############
## Constants ##
###############

#############
## Classes ##
#############

class DefaultPanel(wx.Panel):
	"""
	Menu panel, with all buttons to load data, reset notebook... Contains usefull information and credits.
	"""
	def __init__(self, parent, size : tuple):
		super(DefaultPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		
		# Create features
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.text = wx.StaticText(self,
								  label="Choose the data file you want to load.\nOnly .nc files are allowed",
								  size=(200, 200),
								  style=wx.ALIGN_CENTER
								  )
		font = self.text.GetFont()
		font.PointSize += 5
		font = font.Bold()
		self.text.SetFont(font)
		self.button = wx.Button(self, label="Load data", size=(300, 50))
		# Add features to the panel sizer
		self.sizer.Add(self.text, 0, wx.EXPAND|wx.CENTER, 0)
		self.sizer.Add(self.button, 0, wx.ALL|wx.CENTER, 0)
		self.SetSizer(self.sizer)

	def bind_button(self, event, handler):
		"""
		Assign an event handler to the button.
		"""
		self.button.Bind(event, handler=handler)

class OverviewPanel(wx.Panel):
	"""
	An overview panel to have a better lookup of the variables.
	"""
	def __init__(self, parent, size : tuple, dataset : nc.Dataset, metadata : dict):
		super(OverviewPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		self.dataset = dataset
		self.metadata = metadata
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Create a StaticBox for layout management
		stbox = wx.StaticBox(parent=self, label="Variables")
		font = stbox.GetFont()
		font.PointSize += 5
		stbox.SetFont(font.Bold())
		stbox_sizer = wx.StaticBoxSizer(stbox, wx.HORIZONTAL)
		
		title = wx.StaticText(parent=stbox, label="Choose a variable : ")

		# Combo Box: choosing variables to look at
		l_variables = list(self.metadata.keys())
		self.c_box = wx.ComboBox(
							parent=stbox,
							id=wx.ID_ANY,
							size=(300, 30),
							choices=l_variables,
							style=wx.CB_DROPDOWN | wx.CB_READONLY
							)
		font = font.GetBaseFont()
		font.PointSize -= 5

		title.SetFont(font.Bold())
		self.c_box.SetFont(font)

		stbox_sizer.Add(title, 0, wx.CENTER | wx.ALL, 20)
		stbox_sizer.Add(self.c_box, 0, wx.CENTER | wx.ALL, 20)

		# Dictionary of variable subpanels to hide and show when selecting variables
		self.var_panels = self.generate_subpanels() 
		self.current_panel_name = None

		self.c_box.Bind(wx.EVT_COMBOBOX, handler=self.on_selected)

		# Sizer layout management
		self.sizer.Add(stbox_sizer, 0, wx.EXPAND | wx.ALL , 20)
		for var_name in self.var_panels.keys():
			panel = self.var_panels[var_name]
			panel.Hide()
			self.sizer.Add(panel, 0, wx.EXPAND, 0)
		self.SetSizer(self.sizer)
		self.Fit()

	def generate_subpanels(self):
		"""
		Generate a dictionary of variable subpanels.
		"""
		panels = {}
		for var_name in self.metadata.keys():
			var_meta = self.metadata[var_name]
			panels[var_name] = subpanels.VariablePanel(parent=self, var_name=var_name, var_meta=var_meta)
		return panels

	def on_selected(self, event):
		"""
		ComboBox event handler
		"""
		var_name = self.c_box.GetValue()
		print(var_name, flush=True)
		if self.current_panel_name:
			self.var_panels[self.current_panel_name].Hide()
		self.current_panel_name = var_name
		self.var_panels[var_name].Show()
		self.Layout()


class OptionPanel(wx.Panel):
	"""
	A panel with all the available options to customize the plot.
	Some are mandatory, others are just optional.
	"""
	def __init__(self, parent, size : tuple, dataset : nc.Dataset, metadata : dict):
		super(OptionPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		self.dataset = dataset
		self.metadata = metadata
		self.options = {} # It will gather all the options set by the user
		self.init_options() # Initialize the options dictionary
		self.var_ids = {} # Dictionary with id keys and their corresponing variable

		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		# --------------------------------------- #
		# First StaticBox, general options:
		# Variable / Time index / Level (if necessary)
		stbox_gen = wx.StaticBox(parent=self, label="General")
		stbox_gen_sizer = wx.StaticBoxSizer(stbox_gen, wx.HORIZONTAL)
		
		# Variables
		text_variables = wx.StaticText(parent=stbox_gen, label="Variable : ")
		l_variables = nc_tools.get_variables(self.dataset)
		self.c_box_variables = wx.ComboBox(
									  parent=stbox_gen,
									  id=wx.ID_ANY,
									  choices=l_variables,
									  style=wx.CB_DROPDOWN | wx.CB_READONLY
									  )
		self.var_ids[self.c_box_variables.GetId()] = "variable"

		# Time
		text_time = wx.StaticText(parent=stbox_gen, label="Time index : ")
		timesteps =  nc_tools.get_timesteps(self.dataset)
		self.c_box_time = wx.ComboBox(
									  parent=stbox_gen,
									  id=wx.ID_ANY,
									  choices=timesteps,
									  style=wx.CB_DROPDOWN | wx.CB_READONLY
									  )
		self.var_ids[self.c_box_time.GetId()] = "time_index"

		# Pressure Level (if necessary) 
		if nc_tools.is_pressure_level(meta=self.metadata):
			text_levels = wx.StaticText(parent=stbox_gen, label="Pressure level : ")
			levels = nc_tools.get_pressure_levels(self.dataset)
			self.c_box_levels = wx.ComboBox(
									  		parent=stbox_gen,
									  		id=wx.ID_ANY,
									 	 	choices=levels,
									  		style=wx.CB_DROPDOWN | wx.CB_READONLY
									  		)
			self.var_ids[self.c_box_levels.GetId()] = "pl_index"
		else:
			self.c_box_levels = None

		# StaticBox sizer setup
		stbox_gen_sizer.Add(text_variables, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_gen_sizer.Add(self.c_box_variables, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		stbox_gen_sizer.Add(text_time, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_gen_sizer.Add(self.c_box_time, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		if self.c_box_levels:
			# Add levels to the sizer if dataset contains levels
			stbox_gen_sizer.Add(text_levels, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
			stbox_gen_sizer.Add(self.c_box_levels, 0, wx.ALIGN_CENTER | wx.ALL, 20)

		# --------------------------------------- #
		# Second StaticBox, data corrections
		stbox_data_corr = wx.StaticBox(parent=self, label="Corrections")
		stbox_data_corr_sizer = wx.StaticBoxSizer(stbox_data_corr, wx.HORIZONTAL)

		# Longitude offset
		text_lon_offset = wx.StaticText(parent=stbox_data_corr, label="Longitude offset : ")
		self.te_lon_offset = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=0, style=wx.TE_PROCESS_ENTER, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_lon_offset.GetId()] = "lon_offset"

		# Data multiplicator
		text_coef = wx.StaticText(parent=stbox_data_corr, label="Apply coefficient : ")
		self.te_coef = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=1, style=wx.TE_PROCESS_ENTER, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_coef.GetId()] = "coef"

		# Data offset
		text_data_offset = wx.StaticText(parent=stbox_data_corr, label="Data offset : ")
		self.te_data_offset = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=0, style=wx.TE_PROCESS_ENTER, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_data_offset.GetId()] = "offset"

		# StaticBox sizer setup
		stbox_data_corr_sizer.Add(text_lon_offset, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_lon_offset, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		stbox_data_corr_sizer.Add(text_coef, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_coef, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		stbox_data_corr_sizer.Add(text_data_offset, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_data_offset, 0, wx.ALIGN_CENTER | wx.ALL, 20)

		# --------------------------------------- #
		# Third StaticBox, projection setup

		# --------------------------------------- #
		# Fourth StaticBox, plot options

		# --------------------------------------- #
		# Bindings
		self.Bind(wx.EVT_COMBOBOX, handler=self.on_option_change)
		self.Bind(wx.EVT_TEXT, handler=self.on_option_change)

		# --------------------------------------- #
		# Add element to the main sizer
		self.main_sizer.Add(stbox_gen_sizer, 0, wx.EXPAND | wx.ALL, 20)
		self.main_sizer.Add(stbox_data_corr_sizer, 0, wx.EXPAND | wx.ALL, 20)
		self.SetSizer(self.main_sizer)

	def on_option_change(self, event):
		"""
		Event handler catching all the option changes.
		"""
		element = event.GetEventObject()
		print(self.options, flush=True)
		var = self.var_ids[element.GetId()]
		if var == 'time_index' or var == 'pl_index':
			self.options[var] = element.GetValue().split(" ")[0]
		else:
			self.options[var] = element.GetValue()
		print(self.options, flush=True)
		event.Skip()

	def init_options(self):
		"""
		Initialize the map options.
		"""
		self.options = {
			"variable": nc_tools.get_variables(self.dataset)[0],
			"time_index": 0,
			"pl_index": 0,
			"lon_offset": 0,
			"coef": 1,
			"offset": 0,
			"lon_0": 0,
			"lat_0": 0,
			"llcrnrlat": None,
			"llcrnrlon": None,
			"urcrnrlat": None,
			"urcrnrlon": None,
			"resolution": None,
			"projection": "merc",
			"countries": False,
			"rivers": False,
			"cmap": "seismic",
			"colorbar": False,
			"c_min": 0,
			"c_max": 50,
			"midpoint": 25,
			"plot_type": "mesh"
		}


class PlotPanel(wx.Panel):
	"""
	"""
	def __init__(self, parent, size : tuple):
		super(PlotPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)