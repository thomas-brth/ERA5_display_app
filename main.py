# ERA 5 Graphic User Interface

"""
Links:
http://matplotlib.1069221.n5.nabble.com/Embedding-Basemap-in-a-wx-app-td17935.html
https://pythonspot.com/wxpython-tabs/
https://www.blog.pythonlibrary.org/2010/06/16/wxpython-how-to-switch-between-panels/
https://www.programcreek.com/python/example/4873/wx.MessageBox
Plot colormaps: https://stackoverflow.com/questions/34314356/how-to-view-all-colormaps-available-in-matplotlib
"""

#############
## Imports ##
#############

# Paths fixing
import sys
if __name__ == '__main__':
	sys.path.append("utils")
	sys.path.append("utils\\features")
	sys.path.append("utils\\figure")

# General imports
import os

# GUI imports
import wx

# Custom imports
from utils import nc_tools, wx_tools
from utils.panels import DefaultPanel, OverviewPanel, OptionPanel, PlotPanel
from utils.dialogs import PresetDialog

###############
## Constants ##
###############

GENERAL_SIZE = (1080, 720)
NOTEBOOK_SIZE = (1080, 720)
PANEL_SIZE = (1080, 720)
DEFAULT_POSITION = (200, 50)

#############
## Classes ##
#############

class DisplayApp(wx.App):
	"""
	Top-level app, initializing the frame to be displayed.
	"""
	def __init__(self, title : str, size : tuple = GENERAL_SIZE, position : tuple = DEFAULT_POSITION):
		super(DisplayApp, self).__init__()
		# Default frame style flag, with resizing and maximizing window disabled
		flags = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
		self.frame = DisplayFrame(
								  parent=None,
								  id=wx.ID_ANY,
								  title=title,
								  size=size,
								  position=position,
								  style=flags
								  )
		self.frame.Show(True)

class DisplayFrame(wx.Frame):
	"""
	Main frame containing all the different panels inside a notebook.
	By adding or removing pages from this notebook, it enables the app to be interactive with the user.
	"""
	def __init__(self, parent, id : int, title :str, size : tuple, position : tuple, style):
		super(DisplayFrame, self).__init__(parent=parent, id=id, title=title, size=size, pos=position, style=style)
		self.data_path = None
		self.dataset = None
		self.metadata = {}

		# Icon
		icon = wx.Icon(name="ressources\\logo.ico", type=wx.BITMAP_TYPE_ANY)
		#icon.CopyFromBitmap(wx.Bitmap("ressources\\logo.ico", )
		self.SetIcon(icon)

		# Panels to be used inside the frame
		self.default_panel = None
		self.overview_panel = None
		self.option_panel = None
		self.plot_panel = None

		# Main container and notebook added on it
		self.main_panel = wx.Panel(parent=self, id=wx.ID_ANY, size=NOTEBOOK_SIZE)
		self.notebook = wx.Notebook(parent=self.main_panel, style=wx.NB_BOTTOM)

		# Menu panel
		self.default_panel = DefaultPanel(
										  parent=self.notebook,
										  size=PANEL_SIZE
										  )
		self.default_panel.button_load.Bind(event=wx.EVT_BUTTON, handler=self.open_file_browser)
		self.default_panel.button_pres.Bind(event=wx.EVT_BUTTON, handler=self.show_pres_gen)
		
		# Add panels to each tab
		self.notebook.AddPage(self.default_panel, "Menu")

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(self.notebook, 0, wx.EXPAND, 0)
		self.main_panel.SetSizer(main_sizer)

	def open_file_browser(self, event):
		"""
		Create and show a file browser.
		"""
		wildcard = "netCDF4 files (*.nc)|*.nc|"\
				   "All files (*.*)|*.*"
		flags = wx.FD_OPEN | wx.FD_CHANGE_DIR
		dlg = wx.FileDialog(self, 
							message="Choose a file",
							defaultDir=os.getcwd(),
							defaultFile="",
							wildcard=wildcard,
							style=flags
							)
		if dlg.ShowModal() == wx.ID_OK:
			# Retrieve path from FileDialog window and load the associated dataset
			paths = dlg.GetPaths()
			self.data_path = paths[0]
			self.load_data()

	def load_data(self):
		"""
		Open dataset and get metadata.
		"""
		if self.dataset:
			# If a dataset has already been loaded, delete pages associated with this dataset.
			answer = wx.MessageBox(
								   message="Do you want to continue?\n\
								   All tabs will be reset: your selected options, as well as your plot, will be deleted.",
								   caption="Warning",
								   style= wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION
								   )
			if answer == wx.OK:
				# Continue process and try loading data
				wx_tools.delete_all_excluding(notebook=self.notebook, exclusion_list=["Menu"])
				loading = True
			else:
				wx.MessageBox(message="Data loading process aborted.", caption="Information", style= wx.OK | wx.ICON_INFORMATION)
				loading = False
		else:
			loading = True
		if loading:
			try:
				self.dataset = nc_tools.open_dataset(self.data_path)
				self.metadata = nc_tools.get_meta(self.dataset)
				self.show_overview()
				self.show_options()
			except Exception as e:
				# Catch error and display an error message
				## ADD AN EXECPTION LOG FILE ##
				wx.MessageBox(
							  message=f"Error! Data could not be loaded.\n{e}",
							  caption="Error",
							  style=wx.OK | wx.ICON_ERROR
							  )

	def show_pres_gen(self, event):
		"""
		Show the preset generator dialog.
		"""
		PresetDialog(self, "Preset Generator")

	def show_overview(self):
		"""
		Show the overview panel.
		"""
		self.overview_panel = OverviewPanel(
											parent=self.notebook,
											size=PANEL_SIZE,
											dataset=self.dataset,
											metadata=self.metadata
											)
		self.notebook.AddPage(self.overview_panel, "Data Overview")


	def show_options(self):
		"""
		Show the map options panel.
		"""
		self.option_panel = OptionPanel(
										parent=self.notebook,
										size=PANEL_SIZE,
										dataset=self.dataset,
										metadata=self.metadata
										)
		self.notebook.AddPage(self.option_panel, "Map Options")
		self.option_panel.button.Bind(wx.EVT_BUTTON , handler=self.show_plot)

	def show_plot(self, event):
		"""
		Show the plot panel.
		"""
		wx_tools.delete_all_excluding(notebook=self.notebook, exclusion_list=["Menu", "Data Overview", "Map Options"])
		self.plot_panel = PlotPanel(
									parent=self.notebook,
									size=PANEL_SIZE,
									dataset=self.dataset,
									map_options=self.option_panel.options,
									presets=self.option_panel.presets
									)
		self.plot_panel.draw()
		self.notebook.AddPage(self.plot_panel, "Plot")
		event.Skip()
		
###############
## Functions ##
###############

def main():
	app = DisplayApp(title="ERA 5 display app")
	app.MainLoop()

if __name__ == '__main__':
	main()