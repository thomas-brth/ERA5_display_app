# ERA 5 Graphic User Interface

"""
Links:
http://matplotlib.1069221.n5.nabble.com/Embedding-Basemap-in-a-wx-app-td17935.html
https://pythonspot.com/wxpython-tabs/
https://www.blog.pythonlibrary.org/2010/06/16/wxpython-how-to-switch-between-panels/
https://www.programcreek.com/python/example/4873/wx.MessageBox
"""

#############
## Imports ##
#############

# Paths fixing
import sys
sys.path.append("utils")
sys.path.append("utils\\features")

# General imports
import os

# GUI imports
import wx

# Custom imports
from utils import nc_tools, wx_tools
from utils.panels import DefaultPanel, OverviewPanel, OptionPanel, PlotPanel

###############
## Constants ##
###############

GENERAL_SIZE = (800, 600)
NOTEBOOK_SIZE = (800, 600)
PANEL_SIZE = (800, 600)

#############
## Classes ##
#############

class DisplayApp(wx.App):
	"""
	"""
	def __init__(self, title : str, size : tuple = GENERAL_SIZE):
		super(DisplayApp, self).__init__()
		self.frame = DisplayFrame(
								  parent=None,
								  id=wx.ID_ANY,
								  title=title,
								  size=size,
								  style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER
								  )
		self.frame.SetMinSize(size=(500, 500))
		self.frame.SetMaxSize(size=(1200, 800))
		self.frame.Show(True)

class DisplayFrame(wx.Frame):
	"""
	"""
	def __init__(self, parent, id : int, title :str, size : tuple, style):
		super(DisplayFrame, self).__init__(parent=parent, id=id, title=title, size=size, style=style)
		self.data_path = None
		self.dataset = None
		self.metadata = {}
		self.default_panel = None
		self.overview_panel = None
		self.option_panel = None
		self.plot_panel = None

		# Main container and notebook
		self.main_panel = wx.Panel(parent=self, id=wx.ID_ANY, size=NOTEBOOK_SIZE)
		self.notebook = wx.Notebook(parent=self.main_panel, style=wx.NB_BOTTOM)

		# Menu panel
		self.default_panel = DefaultPanel(parent=self.notebook, size=PANEL_SIZE)
		self.default_panel.bind_button(event=wx.EVT_BUTTON, handler=self.open_file_browser)
		
		# Add panels to each tab
		self.notebook.AddPage(self.default_panel, "Menu")

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(self.notebook, 0, wx.EXPAND, 0)
		self.main_panel.SetSizer(main_sizer)
		self.Bind(wx.EVT_SIZE, handler=self.OnSize)

	def OnSize(self, event):
		"""
		Resize all the panels when the frame is resized.
		"""
		size = self.GetClientSize()
		size[0] = max(size[0], 400)
		size[1] = max(size[1], 400)
		self.main_panel.SetSize(size)
		self.notebook.SetSize(size)

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
			paths = dlg.GetPaths()
			self.data_path = paths[0]
			self.load_data()

	def load_data(self):
		"""
		Open dataset and get metadata.
		"""
		try:
			self.dataset = nc_tools.open_dataset(self.data_path)
			self.metadata = nc_tools.get_meta(self.dataset)
			self.show_overview()
			self.show_options()
		except Exception as e:
			# Catch error and display an error message
			# TO BE IMPLEMENTED #
			wx.MessageBox(f"Error! Data could not be loaded.\n{e}", "Error", wx.OK | wx.ICON_ERROR)
			raise e

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
										size=PANEL_SIZE
										)
		self.notebook.AddPage(self.option_panel, "Map Options")
		
###############
## Functions ##
###############

def main():
	app = DisplayApp(title="ERA 5 display app", size=(500, 500))
	app.MainLoop()

if __name__ == '__main__':
	main()