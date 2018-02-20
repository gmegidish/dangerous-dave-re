import wx
import wxPython

from wxPython.wx import *
from TileManager import *
from LevelRenderer import *

class PreviewDialog(wx.Dialog):

	def __init__(self, parent, title, dlg_size):
		wx.Dialog.__init__(self, parent, -1, title)
		self.SetClientSize(dlg_size)
	
		self.renderer = LevelRenderer(self)
		self.renderer.SetSizeWH(dlg_size[0], dlg_size[1])

	def SetLevelData(self, level):
		self.renderer.SetLevelData(level)

	def SetTileManager(self, manager):
		self.renderer.SetTileManager(manager)
