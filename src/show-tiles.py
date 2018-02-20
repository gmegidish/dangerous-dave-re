import sys
import Image
import string
import ega_palette

def put_tile(image, tiledata, x, y):

	bitmap = [chr(0)] * 256
	for ty in range(16):

		for tx in range(16):

			# get the four bits for this pixel
			c0 = ord(tiledata[(tx >> 3) + (ty << 1) + 0])
			c1 = ord(tiledata[(tx >> 3) + (ty << 1) + 32])
			c2 = ord(tiledata[(tx >> 3) + (ty << 1) + 64])
			c3 = ord(tiledata[(tx >> 3) + (ty << 1) + 96])

			# build up a nibble
			bit = 7 - (tx & 7)
			color = ((c3 >> bit) & 1) << 3
			color = color | (((c2 >> bit) & 1) << 2)
			color = color | (((c1 >> bit) & 1) << 1)
			color = color | (((c0 >> bit) & 1) << 0)
			#image.putpixel((x+tx, y+ty), color)

			bitmap[ty*16 + tx] = chr(color)
	
	s = string.joinfields(bitmap, '')
	smallimage = Image.fromstring("P", (16, 16), s)
	image.paste(smallimage, (x, y))

# egatiles stores tiles used in all levels
f = open("egatiles.dd2", "rb")
tiles = f.read()
f.close()

total_tiles = len(tiles) / 128

width = 13
height = total_tiles / width
if total_tiles % width > 0:
	height = height + 1

im = Image.new("P", (width*16, height*16))
im.im.putpalette("RGB", ega_palette.palette)

for y in range(height):

	print "y %d" % y
	for x in range(width):

		tile_index = (y*width + x)
		tile_offset = tile_index << 7
		tiledata = tiles[tile_offset : tile_offset+128]
		if len(tiledata) < 128:
			break

		put_tile(im, tiledata, x * 16, y * 16)

im.save("egatiles.png")
