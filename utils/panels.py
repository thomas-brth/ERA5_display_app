# Panels module

#############
## Imports ##
#############

# Paths fixing
import os
import sys
if __name__ == '__main__':
	sys.path.append("features")
	sys.path.append("figure")

# GUI imports
import wx
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl

# matplotlib import
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure as MplFig

# Other imports
import netCDF4 as nc # Not used for its functions, only for typing
import json # Used to retrieve map presets

# Custom imports
from features import subpanels
from figure import display_tools
from figure import *
import nc_tools

###############
## Constants ##
###############

MAP_PREVIEW_PATH = "..\\ressources\\images\\maps\\"

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
		self.c_boxes = [] # List of ComboBox used
		self.text_entries = [] # List of text entries used
		self.chk_boxes = [] # List of check boxes used

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
		self.c_boxes.append(self.c_box_variables)

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
		self.c_boxes.append(self.c_box_time)

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
			self.c_boxes.append(self.c_box_levels)
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
		self.te_lon_offset = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=0, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_lon_offset.GetId()] = "lon_offset"
		self.text_entries.append(self.te_lon_offset)

		# Data multiplicator
		text_coef = wx.StaticText(parent=stbox_data_corr, label="Apply coefficient : ")
		self.te_coef = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=1, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_coef.GetId()] = "coef"
		self.text_entries.append(self.te_coef)

		# Data offset
		text_data_offset = wx.StaticText(parent=stbox_data_corr, label="Data offset : ")
		self.te_data_offset = NumCtrl(parent=stbox_data_corr, id=wx.ID_ANY, value=0, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_data_offset.GetId()] = "offset"
		self.text_entries.append(self.te_data_offset)

		# StaticBox sizer setup
		stbox_data_corr_sizer.Add(text_lon_offset, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_lon_offset, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		stbox_data_corr_sizer.Add(text_coef, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_coef, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		stbox_data_corr_sizer.Add(text_data_offset, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.BOTTOM, 20)
		stbox_data_corr_sizer.Add(self.te_data_offset, 0, wx.ALIGN_CENTER | wx.ALL, 20)

		# --------------------------------------- #
		# Third StaticBox, projection setup
		stbox_proj = wx.StaticBox(parent=self, label="Map setup")
		stbox_proj_sizer = wx.StaticBoxSizer(stbox_proj, wx.HORIZONTAL)

		# Panel projection #
		pnl_proj = wx.Panel(parent=stbox_proj)
		pnl_proj_sizer = wx.GridSizer(cols=2, gap=(5, 5))
		
		text_proj = wx.StaticText(parent=pnl_proj, label="Projection : ")
		proj_list = ["moll", "mill", "ortho"]
		self.c_box_proj = wx.ComboBox(
									  parent=pnl_proj,
									  id=wx.ID_ANY,
									  choices=proj_list,
									  style=wx.CB_DROPDOWN | wx.CB_READONLY
									  )
		self.var_ids[self.c_box_proj.GetId()] = "projection"
		self.c_boxes.append(self.c_box_proj)

		text_lon_0 = wx.StaticText(parent=pnl_proj, label="lon_0 : ")
		self.te_lon_0 = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=0, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_lon_0.GetId()] = "lon_0"
		self.text_entries.append(self.te_lon_0)

		text_lat_0 = wx.StaticText(parent=pnl_proj, label="lat_0 : ")
		self.te_lat_0 = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=0, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_lat_0.GetId()] = "lat_0"
		self.text_entries.append(self.te_lat_0)

		text_llcrnrlon = wx.StaticText(parent=pnl_proj, label="llcrnrlon : ")
		self.te_llcrnrlon = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=-180, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_llcrnrlon.GetId()] = "llcrnrlon"
		self.text_entries.append(self.te_llcrnrlon)
		self.te_llcrnrlon.Enable(False)

		text_llcrnrlat = wx.StaticText(parent=pnl_proj, label="llcrnrlat : ")
		self.te_llcrnrlat = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=-90, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_llcrnrlat.GetId()] = "llcrnrlat"
		self.text_entries.append(self.te_llcrnrlat)
		self.te_llcrnrlat.Enable(False)

		text_urcrnrlon = wx.StaticText(parent=pnl_proj, label="urcrnrlon : ")
		self.te_urcrnrlon = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=180, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_urcrnrlon.GetId()] = "urcrnrlon"
		self.text_entries.append(self.te_urcrnrlon)
		self.te_urcrnrlon.Enable(False)

		text_urcrnrlat = wx.StaticText(parent=pnl_proj, label="urcrnrlat : ")
		self.te_urcrnrlat = NumCtrl(parent=pnl_proj, id=wx.ID_ANY, value=90, integerWidth=3, fractionWidth=2)
		self.var_ids[self.te_urcrnrlat.GetId()] = "urcrnrlat"
		self.text_entries.append(self.te_urcrnrlat)
		self.te_urcrnrlat.Enable(False)

		# Sizer setup
		pnl_proj_sizer.Add(text_proj, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.c_box_proj, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_lon_0, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_lon_0, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_lat_0, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_lat_0, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_llcrnrlon, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_llcrnrlon, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_llcrnrlat, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_llcrnrlat, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_urcrnrlon, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_urcrnrlon, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(text_urcrnrlat, 0, wx.ALIGN_CENTER, 20)
		pnl_proj_sizer.Add(self.te_urcrnrlat, 0, wx.ALIGN_CENTER, 20)
		pnl_proj.SetSizer(pnl_proj_sizer)

		# Panel other options #
		pnl_other = wx.Panel(parent=stbox_proj)
		pnl_other_sizer = wx.GridSizer(cols=2, gap=(5, 5))

		text_res = wx.StaticText(parent=pnl_other, label="Resolution : ")
		l_resolutions = ['c', 'l', 'i', 'h', 'f']
		self.c_box_res = wx.ComboBox(
									 parent=pnl_other,
									 id=wx.ID_ANY,
									 choices=l_resolutions,
									 style=wx.CB_DROPDOWN | wx.CB_READONLY,
									 size=(100, 25)
									 )
		self.var_ids[self.c_box_res.GetId()] = "resolution"
		self.c_boxes.append(self.c_box_res)

		self.check_countries = wx.CheckBox(parent=pnl_other, id=wx.ID_ANY, label=" Draw countries")
		self.var_ids[self.check_countries.GetId()] = "countries"
		self.chk_boxes.append(self.check_countries)

		self.check_rivers = wx.CheckBox(parent=pnl_other, id=wx.ID_ANY, label=" Draw rivers")
		self.var_ids[self.check_rivers.GetId()] = "rivers"
		self.chk_boxes.append(self.check_rivers)

		text_cmap = wx.StaticText(parent=pnl_other, label="Colormap : ")
		colormaps = display_tools.get_cmap()
		self.c_box_cmap = wx.ComboBox(
									  parent=pnl_other,
									  id=wx.ID_ANY,
									  choices=colormaps,
									  style=wx.CB_DROPDOWN | wx.CB_READONLY,
									  size=(100, 25)
									  )
		self.var_ids[self.c_box_cmap.GetId()] = "cmap"
		self.c_boxes.append(self.c_box_cmap)

		text_pltype = wx.StaticText(parent=pnl_other, label="Plot type : ")
		plot_types = ["contour", "countourf", "pcolormesh", "streamplot"]
		self.c_box_pltype = wx.ComboBox(
									  parent=pnl_other,
									  id=wx.ID_ANY,
									  choices=plot_types,
									  style=wx.CB_DROPDOWN | wx.CB_READONLY,
									  size=(100, 25)
									  )
		self.var_ids[self.c_box_pltype.GetId()] = "plot_type"
		self.c_boxes.append(self.c_box_pltype)

		self.check_colorbar = wx.CheckBox(parent=pnl_other, id=wx.ID_ANY, label=" Colorbar")
		self.var_ids[self.check_colorbar.GetId()] = "colorbar"
		self.chk_boxes.append(self.check_colorbar)

		self.check_norm = wx.CheckBox(parent=pnl_other, id=wx.ID_ANY, label=" Norm")
		self.var_ids[self.check_norm.GetId()] = "norm"
		# This check box is not added to the list of check boxes because it'll have its own binding.

		text_midpoint = wx.StaticText(parent=pnl_other, label="Midpoint : ")
		self.te_midpoint = IntCtrl(parent=pnl_other, id=wx.ID_ANY, value=25)
		self.var_ids[self.te_midpoint.GetId()] = "midpoint"
		self.text_entries.append(self.te_midpoint)
		self.te_midpoint.Enable(False)

		text_min = wx.StaticText(parent=pnl_other, label="Min : ")
		self.te_min = IntCtrl(parent=pnl_other, id=wx.ID_ANY, value=0)
		self.var_ids[self.te_min.GetId()] = "c_min"
		self.text_entries.append(self.te_min)
		self.te_min.Enable(False)

		text_max = wx.StaticText(parent=pnl_other, label="Max : ")
		self.te_max = IntCtrl(parent=pnl_other, id=wx.ID_ANY, value=50)
		self.var_ids[self.te_max.GetId()] = "c_max"
		self.text_entries.append(self.te_max)
		self.te_max.Enable(False)

		# Sizer setup
		pnl_other_sizer.Add(text_res, 0)
		pnl_other_sizer.Add(self.c_box_res, 0)
		pnl_other_sizer.Add(self.check_countries, 0)
		pnl_other_sizer.Add(self.check_rivers, 0)
		pnl_other_sizer.Add(text_cmap, 0)
		pnl_other_sizer.Add(self.c_box_cmap, 0)
		pnl_other_sizer.Add(text_pltype, 0)
		pnl_other_sizer.Add(self.c_box_pltype, 0)
		pnl_other_sizer.Add(self.check_colorbar, 0)
		pnl_other_sizer.Add(self.check_norm, 0)
		pnl_other_sizer.Add(text_midpoint, 0)
		pnl_other_sizer.Add(self.te_midpoint, 0)
		pnl_other_sizer.Add(text_min, 0)
		pnl_other_sizer.Add(self.te_min, 0)
		pnl_other_sizer.Add(text_max, 0)
		pnl_other_sizer.Add(self.te_max, 0)
		pnl_other.SetSizer(pnl_other_sizer)

		# StaticBox Sizer setup
		stbox_proj_sizer.Add(pnl_proj, 0, wx.ALL, 20)
		stbox_proj_sizer.Add(pnl_other, 0, wx.ALL, 20)

		# --------------------------------------- #
		# PLot Button

		self.button = wx.Button(parent=self, label="Draw", size=(200, 30))

		# --------------------------------------- #
		# Bindings
		for c_box in self.c_boxes:
			c_box.Bind(wx.EVT_COMBOBOX, handler=self.on_option_change)
		for te in self.text_entries:
			te.Bind(wx.EVT_TEXT, handler=self.on_option_change)
		for chk in self.chk_boxes:
			chk.Bind(wx.EVT_CHECKBOX, handler=self.on_option_change)
		self.check_norm.Bind(wx.EVT_CHECKBOX, handler=self.on_norm_change)

		# --------------------------------------- #
		# Add element to the main sizer
		self.main_sizer.Add(stbox_gen_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
		self.main_sizer.Add(stbox_data_corr_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
		self.main_sizer.Add(stbox_proj_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
		self.main_sizer.Add(self.button, 0, wx.ALIGN_CENTER | wx.ALL, 20)
		self.SetSizer(self.main_sizer)

	def on_option_change(self, event):
		"""
		Event handler catching all the option changes.
		"""
		element = event.GetEventObject()
		_id = element.GetId()
		var_name = self.var_ids[_id]
		if var_name == 'time_index' or var_name == 'pl_index':
			val = int(element.GetValue().split(" ")[0])
		elif var_name == 'projection':
			val = element.GetValue().split(" ")[0]
			proj_without_boundaries = ['sinu', 'moll', 'hammer', 'npstere', 'spstere', 'nplaea', 'splaea', 'npaeqd', 'spaeqd', 'robin', 'eck4', 'kav7', 'mbtfpq']
			if val in proj_without_boundaries:
				self.te_llcrnrlon.Enable(False)
				self.te_llcrnrlat.Enable(False)
				self.te_urcrnrlon.Enable(False)
				self.te_urcrnrlat.Enable(False)
				self.options['boundaries'] = False
			else:
				self.te_llcrnrlon.Enable(True)
				self.te_llcrnrlat.Enable(True)
				self.te_urcrnrlon.Enable(True)
				self.te_urcrnrlat.Enable(True)
				self.options['boundaries'] = True
		else:
			val = element.GetValue()
		self.update_option(var_name, val)
		print(self.options, flush=True)
		event.Skip()

	def on_norm_change(self, event):
		"""
		Enable or disable text entries for colorbar setup.
		"""
		chk_box = event.GetEventObject()
		val = chk_box.GetValue()
		self.options[self.var_ids[chk_box.GetId()]] = val
		self.te_midpoint.Enable(val)
		self.te_min.Enable(val)
		self.te_max.Enable(val)
		event.Skip()

	def init_options(self):
		"""
		Initialize the map options.
		"""
		self.options = {
			"variable": nc_tools.get_variables(self.dataset)[0],
			"time_index": None,
			"pl_index": None,
			"lon_offset": 0,
			"coef": 1,
			"offset": 0,
			"lon_0": 0,
			"lat_0": 0,
			"boundaries": False,
			"llcrnrlat": -90,
			"llcrnrlon": -180,
			"urcrnrlat": 90,
			"urcrnrlon": 180,
			"resolution": 'i',
			"projection": "moll",
			"countries": False,
			"rivers": False,
			"cmap": "seismic",
			"colorbar": False,
			"norm": False,
			"c_min": 0,
			"c_max": 50,
			"midpoint": 25,
			"plot_type": "mesh"
		}

	def update_option(self, var_name : str, val):
		"""
		Update the options: assign value :val: to the option associated with element with respect to the associated variable.
		"""
		try:
			self.options[var_name] = val
		except Exception as e:
			raise e

	def bind_draw_button(self, handler):
		"""
		Bind the draw button with an external handler.
		"""
		self.button.Bind(wx.EVT_BUTTON , handler=handler)

class PlotPanel(wx.Panel):
	"""
	A panel on which is drawn the map with wanted data.
	"""
	def __init__(self, parent, size : tuple, dataset : nc.Dataset, map_options : dict, tb_option : bool = True):
		super(PlotPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		self.dataset = dataset
		self.map_options = map_options

		self.figure = MplFig()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self, -1, self.figure)

		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.main_sizer.Add(self.canvas, 0, wx.EXPAND)

		self.toolbar = None
		if tb_option:
			self.add_toolbar()
			self.main_sizer.Add(self.toolbar, 0, wx.EXPAND | wx.LEFT, 20)
			self.toolbar.update()

		self.SetSizer(self.main_sizer)

	def draw(self):
		"""
		Draw the data and the map.
		"""
		# Create figure		
		fig = Figure(figure=self.figure, ax=self.axes, dataset=self.dataset, map_options=self.map_options)
		fig.plot_data()
		self.figure.canvas.draw()

	def add_toolbar(self):
		"""
		Add a toolbar to the Canvas.
		"""
		self.toolbar = NavigationToolbar2Wx(self.canvas)
		self.toolbar.Realize()

		tw, th = self.toolbar.GetSize()
		cw, ch = self.canvas.GetSize()

		self.toolbar.SetSize(wx.Size(cw, ch))

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)