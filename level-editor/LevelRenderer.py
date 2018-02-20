import wx
import wxPython

from LevelData import *
from wxPython.wx import *

class LevelRenderer(wx.ScrolledWindow):

	def __init__(self, parent, filename=None):
		wx.ScrolledWindow.__init__(self, parent, -1)

		self.level = LevelData()
		self.tiles = None

		self.left_down = 0

		self.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.SetScrollbars(0, 0, 0, 0)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)

		if filename:
			self.LoadLevel(filename)

	def SetTileManager(self, manager):
		self.tiles = manager
		# force

	def CopyTilesFromManager(self, pt):
		selected = self.tiles.GetSelectedTiles()

		ptx = pt.x / 16
		pty = pt.y / 16

		dc = wx.ClientDC(self)
		for y in range(selected[1], selected[3] + 1):
			for x in range(selected[0], selected[2] + 1):
				c = (y*13 + x)

				self.level.SetTile((ptx + x - selected[0], pty + y - selected[1]), c)

				dx = (ptx + x - selected[0]) * 16
				dy = (pty + y - selected[1]) * 16
				self.tiles.DrawTile(dc, (x, y), (dx, dy))

	def OnLeftDown(self, evt):
		self.left_down = 1
		self.CopyTilesFromManager(evt.GetPosition())

	def OnLeftUp(self, evt):
		self.left_down = 0

	def OnMotion(self, evt):
		if self.left_down:
			self.CopyTilesFromManager(evt.GetPosition())

	def LoadLevel(self, filename):
		self.level.LoadDD2(filename)
		self.SetScrollbars(20, 20, self.level.GetWidth()*16/20, self.level.GetHeight()*16/20)

	def GetLevelData(self):
		return self.level

	def SetLevelData(self, level):
		self.level = level
		self.SetScrollbars(20, 20, self.level.GetWidth()*16/20, self.level.GetHeight()*16/20)

	def OnPaint(self, evt):

		dc = wx.PaintDC(self)
		self.PrepareDC(dc)

		if self.level and self.tiles:

			for y in range(self.level.GetHeight()):

				dy = (y * 16)
				for x in range(self.level.GetWidth()):
		
					dx = (x * 16)

					tile = self.level.GetTile((x, y))
					tx = (tile % 13)
					ty = (tile / 13)
					txy = (tx, ty)

					self.tiles.DrawTile(dc, txy, (dx, dy))

