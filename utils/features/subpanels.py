# Sub-pannels module, to be used inside main panels

#############
## Imports ##
#############

import wx

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
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		# Title font initialization
		title_font = wx.Font()
		
		# Create the different text widgets
		self.sizer.AddSpacer(15)
		title = wx.StaticText(self, label=f"Description of the variable {var_name}", style=wx.ALIGN_CENTER)
		title.SetFont(title_font.Bold())
		self.sizer.Add(title, 0, wx.EXPAND, 20)
		self.sizer.AddSpacer(15)
		
		dimensions = wx.StaticText(self, label=f"Dimensions : {var_meta['dimensions']}")
		self.sizer.Add(dimensions, 0, wx.LEFT, 20)
		
		shape = wx.StaticText(self, label=f"Shape : {var_meta['shape']}")
		self.sizer.Add(shape, 0, wx.LEFT, 20)

		self.sizer.AddSpacer(15)
		attributes_title = wx.StaticText(self, label="Attributes", style=wx.ALIGN_CENTER)
		attributes_title.SetFont(title_font.Bold())
		self.sizer.Add(attributes_title, 0, wx.EXPAND, 20)
		self.sizer.AddSpacer(15)

		attr_dict = var_meta['attributes']
		for attr in attr_dict.keys():
			attr_text = wx.StaticText(self, label=f"{attr} : {attr_dict[attr]}")
			self.sizer.Add(attr_text, 0, wx.LEFT, 20)

		self.SetSizer(self.sizer)

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)