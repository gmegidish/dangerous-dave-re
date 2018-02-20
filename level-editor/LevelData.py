import struct

class LevelData:

	def __init__(self):
		self.__w = 0
		self.__h = 0
		self.__data = []

	def LoadDD2(self, filename):
		
		f = open(filename, 'rb')
		raw = f.read()
		f.close()

		dd2_w = struct.unpack('<h', raw[4:6])[0]
		dd2_h = struct.unpack('<h', raw[6:8])[0]

		self.__w = dd2_w
		self.__h = dd2_h
		self.__data = []

		for y in range(dd2_h):

			ar = []
			for x in range(dd2_w):

				offset = 0x24 + ((y * dd2_w + x) * 2)
				tile = struct.unpack('<h', raw[offset:offset+2])[0]
				ar.append(tile)

			self.__data.append(ar)

	def GetTile(self, xy):
		c = self.__data[xy[1]][xy[0]]
		return c

	def SetTile(self, xy, c):
		self.__data[xy[1]][xy[0]] = c

	def GetWidth(self):
		return self.__w

	def GetHeight(self):
		return self.__h
