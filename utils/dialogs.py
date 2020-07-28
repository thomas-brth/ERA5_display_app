# Dialogs module

#############
## Imports ##
#############

# wxPython import
import wx

# Custom import
from features.subpanels import PresetPanel

###############
## Constants ##
###############

#############
## Classes ##
#############

class PresetDialog(wx.Dialog):
	"""
	Preset generator dialog.

	This is a modeless dialog, i.e. it is not returning any value.
	"""
	def __init__(self, parent, title : str, size : tuple = (400, 400)):
		super(PresetDialog, self).__init__(parent=parent, id=wx.ID_ANY, title=title)
		self.parent = parent
		# Create sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		# Create custom panel
		self.panel = PresetPanel(self, size)

		# Sizer setup
		self.sizer.Add(self.panel, 0, wx.EXPAND, 0)
		self.SetSizerAndFit(self.sizer)

		self.Show()

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.")