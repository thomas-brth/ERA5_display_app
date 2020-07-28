# Sub-pannels module, to be used inside main panels

#############
## Imports ##
#############

# wxPython import
import wx

# matplotlib import
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap

# Other imports
import os
import json

###############
## Constants ##
###############

#############
## Classes ##
#############

class VariablePanel(wx.Panel):
	"""
	Panel used to display information on the different variables available.
	This subpanel is meant to be displayed inside the overview panel.
	"""
	def __init__(self, parent, var_name : str, var_meta : dict):
		super(VariablePanel, self).__init__(parent=parent, id=wx.ID_ANY)
		self.parent = parent
		self.var_name = var_name
		self.var_meta = var_meta
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)

		# First StaticBox with general information
		stbox_gen = wx.StaticBox(parent=self, label=f"Description of the variable {var_name}", size=(600, 200))
		font = stbox_gen.GetFont()
		font.PointSize += 5
		stbox_gen.SetFont(font.Bold())
		stbox_gen_sizer = wx.StaticBoxSizer(stbox_gen, wx.VERTICAL)
		
		dimensions = wx.StaticText(stbox_gen, label=f"Dimensions : {var_meta['dimensions']}")
		shape = wx.StaticText(stbox_gen, label=f"Shape : {var_meta['shape']}")
		
		font = font.GetBaseFont()
		font.PointSize -= 5
		font.MakeItalic()
		dimensions.SetFont(font)
		shape.SetFont(font)

		stbox_gen_sizer.Add(dimensions, 0, wx.LEFT, 20)
		stbox_gen_sizer.Add(shape, 0, wx.LEFT, 20)

		# Second StaticBox with attributes information
		stbox_attr = wx.StaticBox(parent=self, label="Attributes", size=(600, 350))
		font = stbox_attr.GetFont()
		font.PointSize += 5
		stbox_attr.SetFont(font.Bold())
		stbox_attr_sizer = wx.StaticBoxSizer(stbox_attr, wx.VERTICAL)

		font = font.GetBaseFont()
		font.PointSize -= 5
		font.MakeItalic()

		attr_dict = var_meta['attributes']
		for attr in attr_dict.keys():
			attr_text = wx.StaticText(stbox_attr, label=f"{attr} : {attr_dict[attr]}")
			attr_text.SetFont(font)
			stbox_attr_sizer.Add(attr_text, 0, wx.LEFT, 20)

		self.main_sizer.Add(stbox_gen_sizer, 0, wx.LEFT, 20)
		self.main_sizer.Add(stbox_attr_sizer, 0, wx.LEFT, 20)

		self.SetSizer(self.main_sizer)

class PresetPanel(wx.Panel):
	"""
	A panel for preset generator dialog.
	"""
	def __init__(self, parent, size : tuple):
		super(PresetPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		self.current_args = {}

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Description
		self.te_desc = wx.TextCtrl(parent=self, id=wx.ID_ANY, value="Enter a description")
		
		# Filename
		self.te_filename = wx.TextCtrl(parent=self, id=wx.ID_ANY, value="Enter a filename (without extension)")

		# Sub panel
		sub_panel = wx.Panel(parent=self, id=wx.ID_ANY)
		sub_sizer = wx.GridSizer(cols=2, gap=(5, 5))
		text_name = wx.StaticText(parent=sub_panel, label="Argument name")
		text_val = wx.StaticText(parent=sub_panel, label="Argument value")
		self.te_name = wx.TextCtrl(parent=sub_panel, id=wx.ID_ANY, value="", style=wx.TE_CENTRE)
		self.te_val = wx.TextCtrl(parent=sub_panel, id=wx.ID_ANY, value="", style=wx.TE_CENTRE)
		self.button_add = wx.Button(parent=sub_panel, label="Add")
		self.button_reset = wx.Button(parent=sub_panel, label="Reset")

		sub_sizer.Add(text_name, 0, wx.ALIGN_CENTER, 0)
		sub_sizer.Add(text_val, 0, wx.ALIGN_CENTER, 0)
		sub_sizer.Add(self.te_name, 0, wx.ALIGN_CENTER, 0)
		sub_sizer.Add(self.te_val, 0, wx.ALIGN_CENTER, 0)
		sub_sizer.Add(self.button_add, 0, wx.ALIGN_CENTER, 0)
		sub_sizer.Add(self.button_reset, 0, wx.ALIGN_CENTER, 0)
		sub_panel.SetSizer(sub_sizer)

		# Entered arguments
		self.te_arguments = wx.TextCtrl(parent=self, id=wx.ID_ANY, style=wx.TE_MULTILINE | wx.VSCROLL | wx.TE_READONLY)

		# Process button
		self.button_process = wx.Button(parent=self, label="Process", size=(200, 50))

		# Buttons binding
		self.button_add.Bind(event=wx.EVT_BUTTON, handler=self.on_add)
		self.button_reset.Bind(event=wx.EVT_BUTTON, handler=self.on_reset)

		# Main sizer setup
		self.sizer.Add(self.te_desc, 0, wx.EXPAND | wx.ALL, 10)
		self.sizer.Add(self.te_filename, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		self.sizer.Add(sub_panel, 0, wx.CENTER | wx.ALL, 10)
		self.sizer.Add(self.te_arguments, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		self.sizer.Add(self.button_process, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		self.SetSizer(self.sizer)

	def on_add(self, event):
		"""
		Called when the add button is pressed.
		"""
		arg_name = self.te_name.GetValue()
		arg_value = self.te_val.GetValue()
		self.current_args[arg_name] = arg_value
		print(f"{arg_name} : {arg_value}", flush=True)
		self.update_arguments(arg_name, arg_value)

	def on_reset(self, event):
		"""
		Called when the reset button is pressed.
		"""
		self.te_arguments.ChangeValue("")

	def update_arguments(self, arg_name : str, arg_value : str):
		"""
		Update TextCtrl displaying entered arguments.
		"""
		current_display = self.te_arguments.GetValue()
		self.te_arguments.ChangeValue(current_display+f"{arg_name} : {arg_value}\n")
	
	@staticmethod
	def preset_formatter(preset_file : str, filename : str, description : str, args : dict):
		"""
		Format information, load the presets file and add them.
		"""
		with open(preset_file, 'r') as foo:
			map_presets = json.load(foo)
			foo.close()
	
		preset_name = filename.split(".")[0]
		temp_dict = {}
		temp_dict["description"] = description
		temp_dict["args"] = args
		temp_dict["filename"] = filename
		map_presets[preset_name] = temp_dict
		
		with open(preset_file, 'w') as foo:
			json.dump(map_presets, foo, indent=4)
			foo.close()

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)