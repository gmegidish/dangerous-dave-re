import sys
import Image
import string
import ega_palette

MAGIC = 0x33b0

def put_tile(image, tiledata, x, y):

	bitmap = [chr(0)] * (48*48)
	for ty in range(48):

		for tx in range(48):

			# get the four bits for this pixel
			c0 = ord(tiledata[(tx >> 3) + (ty * 6) + MAGIC*0])
			c1 = ord(tiledata[(tx >> 3) + (ty * 6) + MAGIC*1])
			c2 = ord(tiledata[(tx >> 3) + (ty * 6) + MAGIC*2])
			c3 = ord(tiledata[(tx >> 3) + (ty * 6) + MAGIC*3])

			# build up a nibble
			bit = 7 - (tx & 7)
			color = ((c3 >> bit) & 1) << 3
			color = color | (((c2 >> bit) & 1) << 2)
			color = color | (((c1 >> bit) & 1) << 1)
			color = color | (((c0 >> bit) & 1) << 0)

			bitmap[ty*48 + tx] = chr(color)
	
	s = string.joinfields(bitmap, '')
	smallimage = Image.fromstring("P", (48, 48), s)
	image.paste(smallimage, (x, y))

f = open("dave.exe", "rb")
f.seek(0x18a60)
data = f.read()
f.close()

im = Image.new("P", (48*5, 48*8))
im.im.putpalette("RGB", ega_palette.palette)
x = 0
y = 0

offset = 0
while y < 8:

	tile = data[offset:]
	offset = offset + (6*48)

	put_tile(im, tile, x*48, y*48)
	x = x + 1
	if x == 5:
		x = 0
		y = y + 1

im.save("death-sequences.png")
