import sys
import Image
import string
import ega_palette

def unrle(rle):
	raw = ""
	offset = 0

	while offset < len(rle):

		key = ord(rle[offset]) | (ord(rle[offset + 1]) << 8)

		if key == 0xfefe:
			# rlew
			times = ord(rle[offset + 2]) | (ord(rle[offset + 3]) << 8)
			value = rle[offset + 4 : offset + 6]
			offset = offset + 6

			for i in range(times):
				raw = raw + value 
		else:
			# literal
			raw = raw + rle[offset:offset+2]
			offset = offset + 2

	return raw

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

# open the wanted level
f = open(sys.argv[1], "rb")
level = unrle(f.read())
f.close()

print "Level unpacked to %d bytes" % len(level)

width = ord(level[4]) | (ord(level[5]) << 8)
height = ord(level[6]) | (ord(level[7]) << 8)
height = height - 1

im = Image.new("P", (width*16, height*16))
im.im.putpalette("RGB", ega_palette.palette)

for y in range(height):

	print "\rRendering Y=%d" % y,
	for x in range(width):

		offset = 0x24 + (y * width * 2) + (x * 2)
		tile_index = (ord(level[offset])) | (ord(level[offset + 1]) << 8)
		tile_offset = tile_index * 128

		if True:
			offset = offset + (width * height * 2)
			tag = (ord(level[offset])) | (ord(level[offset + 1]) << 8)
			if tag > 0:
				print "x=%d y=%d tag=%d" % (x, y, tag)
				if tag == 16:
					print "poewrup"
					tile_offset = 1

		tiledata = tiles[tile_offset : tile_offset+128]
		assert len(tiledata) == 128
		put_tile(im, tiledata, x * 16, y * 16)

print offset
im.save("%s.png" % sys.argv[1])
