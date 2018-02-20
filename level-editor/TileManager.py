import wx
import wxPython
from wxPython.wx import *

class TileManager(wx.ScrolledWindow):

	def __init__(self, parent, filename):

		wx.ScrolledWindow.__init__(self, parent, -1)

		set = wx.Bitmap(filename)

		self.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.SetScrollbars(20, 20, set.GetWidth()/20, set.GetHeight()/20)

		self.tileset = set

		self.selected_root = None
		self.selected_wide = 0
		self.selected_high = 0
		self.left_down = 0

		self.dc = wx.MemoryDC()
		self.dc.SelectObject(self.tileset)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)

	def FindTile(self, pt):
		tx = pt.x / 16
		ty = pt.y / 16
		return (tx, ty)

	def GetSelectedTiles(self):
		return (self.selected_root[0], self.selected_root[1], self.selected_root[0] + self.selected_wide - 1, self.selected_root[1] + self.selected_high - 1)

	def DrawSelectionMark(self, dc, show=false):

		if self.selected_root:

			dc.BeginDrawing()

			if show:

				# show rectangle
				dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0), wxTRANSPARENT))
				dc.SetPen(wx.WHITE_PEN)

				rect = wx.Rect(self.selected_root[0]*16, self.selected_root[1]*16, self.selected_wide*16, self.selected_high*16)
				dc.DrawRectangleRect(rect)

				rect = wx.Rect(self.selected_root[0]*16+1, self.selected_root[1]*16+1, self.selected_wide*16, self.selected_high*16)
				dc.DrawRectangleRect(rect)

			else:

				# clear rectangle
				dc.Blit((0, 0), (self.tileset.GetWidth(), self.tileset.GetHeight()), self.dc, (0, 0))

	def OnLeftDown(self, evt):
	        tile = self.FindTile(evt.GetPosition())
		if tile:
			self.DrawSelectionMark(wx.ClientDC(self), false)
			self.selected_root = tile
			self.selected_wide = 1
			self.selected_high = 1
			self.DrawSelectionMark(wx.ClientDC(self), true)
			self.left_down = 1

	def OnLeftUp(self, evt):
		self.left_down = 0

	def OnMotion(self, evt):

		if self.left_down:
			tile = self.FindTile(evt.GetPosition())
			if tile:
				
				# check if possible combination
				if tile[0] >= self.selected_root[0] and tile[1] >= self.selected_root[1]:
					self.DrawSelectionMark(wx.ClientDC(self), false)
					self.selected_wide = tile[0] - self.selected_root[0] + 1
					self.selected_high = tile[1] - self.selected_root[1] + 1
					self.DrawSelectionMark(wx.ClientDC(self), true)

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		self.PrepareDC(dc)
		dc.Blit((0, 0), (self.tileset.GetWidth(), self.tileset.GetHeight()), self.dc, (0, 0))
		self.DrawSelectionMark(dc, true)

	def DrawTile(self, dc, tile, xy):

		# 13 tiles across
		tx = tile[0] * 16
		ty = tile[1] * 16
		dc.Blit(xy, (16, 16), self.dc, (tx, ty))
