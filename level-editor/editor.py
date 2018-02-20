#!/usr/bin/python

import wx
import sys
import struct
import wxPython

from LevelData import *
from TileManager import *
from LevelRenderer import *
from PreviewDialog import *

from wxPython.wx import *

ID_ABOUT   = 101
ID_OPEN    = 102
ID_SAVE    = 103
ID_SAVEAS  = 104
ID_EXIT    = 105
ID_PREVIEW = 106

class TileEditorMainWindow(wxFrame):

	def __init__(self, parent, id, title):
		#wx.InitAllImageHandlers()

		wxFrame.__init__(self, parent, -1, title, size=(720, 540), \
        		style=wxDEFAULT_FRAME_STYLE | wxNO_FULL_REPAINT_ON_RESIZE)

		# status bar
		self.CreateStatusBar(2)
		self.SetStatusWidths([-1, 150])
		self.SetStatusText("Idle")

		# events
		EVT_MENU(self, ID_OPEN, self.OpenFile)
		EVT_MENU(self, ID_EXIT, self.Exit)
		EVT_MENU(self, ID_PREVIEW, self.Preview)

		# register used ids
		wxRegisterId(ID_OPEN)
		wxRegisterId(ID_SAVE)
		wxRegisterId(ID_SAVEAS)
		wxRegisterId(ID_ABOUT)
		wxRegisterId(ID_EXIT)
		wxRegisterId(ID_PREVIEW)

		# menu
		self.filemenu = wxMenu()
		self.filemenu.Append(ID_OPEN, '&Open\tCtrl+O', "Open...")
		self.filemenu.AppendSeparator()
		self.filemenu.Append(ID_EXIT, 'E&xit\tAlt-X', "Quit editor")

		self.editmenu = wxMenu()
		self.editmenu.Append(ID_PREVIEW, '&Preview\tCtrl+P', 'Preview...')

		menuBar = wxMenuBar()
		menuBar.Append(self.filemenu, "&File")
		menuBar.Append(self.editmenu, "&Edit")
		self.SetMenuBar(menuBar)

		# splitter and left frame
		splitter = wx.SplitterWindow(self, -1, style=wx.NO_3D|wx.SP_3D)
        
		self.tile_manager = TileManager(splitter, "tiles.png")

		self.level_renderer = LevelRenderer(splitter, "level01.dd2")
		self.level_renderer.SetTileManager(self.tile_manager)
		
		splitter.SplitVertically(self.tile_manager, self.level_renderer, 208+16)
		splitter.SetMinimumPaneSize(50)

		self.Show(True)
		self.Enable(True)

	def Preview(self, event):

		win = PreviewDialog(self, "Level Preview", (240, 160))
		win.SetTileManager(self.tile_manager)
		win.SetLevelData(self.level_renderer.GetLevelData())
		win.ShowModal()
		win.Destroy()

	def OpenFile(self, event):
		dlg = wxFileDialog(self, "Open level", ".", "", "DD2|*.dd2|All Files|*.*", wxOPEN)

		if dlg.ShowModal() == wxID_OK:
			self.level_renderer.LoadLevel(dlg.GetPath())

		dlg.Destroy()

	def Exit(self, event):

		#if self.OnClose():
		sys.exit()

def run():
	app = wxPySimpleApp()
	frame = TileEditorMainWindow(None, -1, "editor")
	app.MainLoop()

if __name__ == "__main__":
	run()

