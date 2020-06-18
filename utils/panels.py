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

# Custom imports
from features import subpanels

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
		self.SetBackgroundColour('blue')
		
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
		self.Fit()

	def bind_button(self, event, handler):
		"""
		Assign an event handler to the button.
		"""
		self.button.Bind(event, handler=handler)

class OverviewPanel(wx.Panel):
	"""
	An overview panel to have a better lookup of the variables.
	"""
	def __init__(self, parent, size : tuple, dataset, metadata : dict):
		super(OverviewPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)
		self.parent = parent
		self.SetBackgroundColour('green')

		self.dataset = dataset
		self.metadata = metadata
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Combo Box: choosing variables to look at
		l_variables = list(self.metadata.keys())
		self.c_box = wx.ComboBox(
							parent=self,
							id=wx.ID_ANY,
							size=(300, 30),
							choices=l_variables,
							style=wx.CB_DROPDOWN | wx.CB_READONLY
							)

		# Dictionary of variable subpanels to hide and show when selecting variables
		self.var_panels = self.generate_subpanels() 
		self.current_panel_name = None

		self.c_box.Bind(wx.EVT_COMBOBOX, handler=self.on_selected)

		# Sizer layout management
		self.sizer.AddSpacer(50)
		self.sizer.Add(self.c_box, 0, wx.ALIGN_CENTER, 0)
		self.sizer.AddSpacer(50)
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
			panels[var_name] = subpanels.VariablePanel(parent=self, size=(500, 370), var_name=var_name, var_meta=var_meta)
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
	"""
	def __init__(self, parent, size : tuple):
		super(OptionPanel, self).__init__(parent=parent, id=wx.ID_ANY, size=size)

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