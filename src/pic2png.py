import sys
import Image
import string
import ega_palette

f = open(sys.argv[1], "rb")
f.seek(8)
raw = f.read()
f.close()

MAGIC = (320*200 >> 3)

bitmap = [chr(0)] * 64000
for y in range(200):
	for x in range(320):
		# get the four bits for tis pixel
		c0 = ord(raw[(x >> 3) + (y * 40) + MAGIC*0])
		c1 = ord(raw[(x >> 3) + (y * 40) + MAGIC*1])
		c2 = ord(raw[(x >> 3) + (y * 40) + MAGIC*2])
		c3 = ord(raw[(x >> 3) + (y * 40) + MAGIC*3])

		# build up a nibble
		bit = 7 - (x & 7)
		color = ((c3 >> bit) & 1) << 3
		color = color | (((c2 >> bit) & 1) << 2)
		color = color | (((c1 >> bit) & 1) << 1)
		color = color | (((c0 >> bit) & 1) << 0)

		bitmap[y*320 + x] = chr(color)
		
s = string.joinfields(bitmap, '')
im = Image.fromstring("P", (320, 200), s)
im.im.putpalette("RGB", ega_palette.palette)
im.save("%s.png" % sys.argv[1])

