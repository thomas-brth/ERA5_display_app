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

###############
## Functions ##
###############

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)