# Additional wx custom tools

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

###############
## Functions ##
###############

## Notebook tools ##
def search_for_page(notebook : wx.Notebook, page_name : str):
	"""
	Search for a page with a specific name inside the notebook.
	"""
	n_pages = notebook.GetPageCount()
	l_pages = [notebook.GetPageText(i) for i in range (n_pages)]
	return page_name in l_pages

def delete_all_excluding(notebook : wx.Notebook, exclusion_list : list):
	"""
	Delete all pages in the notebook, except specified ones.
	:exclusion_list: is a list of string, containing some page names.
	"""
	if exclusion_list:
		l_index = []
		n_pages = notebook.GetPageCount()
		for i in range (n_pages):
			if notebook.GetPageText(i) not in exclusion_list:
				l_index.append(i) # Gather index of pages to delete
		l_index.sort(reverse=True)
		for index in l_index:
			notebook.DeletePage(index)
	else:
		notebook.DeleteAllPages()

## Bitmaps and Images tools ##
def rescale_image(image : wx.Image, max_width : int, max_height : int):
	"""
	Rescale a wx.Image and return a wx.Bitmap.
	"""
	width, height = image.GetSize()
	ratio = width/height
	new_width = int(ratio*max_height)
	new_height = int(max_width/ratio)
	if new_width <= max_width:
		image.Rescale(new_width, max_height, wx.IMAGE_QUALITY_HIGH)
	else:
		image.Rescale(max_width, new_height, wx.IMAGE_QUALITY_HIGH)
	return wx.Bitmap(image)

def main():
	pass

if __name__ == '__main__':
	main()
else:
	print(f"Module {__name__} imported.", flush=True)