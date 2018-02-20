import sys
import Image
import string
import ega_palette

def put_tile(image, tiledata, x, y, w, h):

	BIG = (w*h >> 3)

	bitmap = [chr(0)] * (w*h)
	for ty in range(h):

		yoffset = ty * (w >> 3)

		for tx in range(w):

			# get the four bits for this pixel
			c0 = ord(tiledata[(tx >> 3) + yoffset + BIG*0])
			c1 = ord(tiledata[(tx >> 3) + yoffset + BIG*1])
			c2 = ord(tiledata[(tx >> 3) + yoffset + BIG*2])
			c3 = ord(tiledata[(tx >> 3) + yoffset + BIG*3])

			# build up a nibble
			bit = 7 - (tx & 7)
			color = ((c3 >> bit) & 1) << 3
			color = color | (((c2 >> bit) & 1) << 2)
			color = color | (((c1 >> bit) & 1) << 1)
			color = color | (((c0 >> bit) & 1) << 0)

			bitmap[ty*w + tx] = chr(color)
	
	s = string.joinfields(bitmap, '')
	smallimage = Image.fromstring("P", (w, h), s)
	image.paste(smallimage, (x, y))

BREAKER = (0, 0)

SPRITE_SIZES=[
	(56, 80), (32, 80), (56, 80), (32, 80), (56, 80), 
	(32, 80), (56, 80), (32, 80)
]

SPRITE_SIZES_DAVE=[
	(24, 32), # standing right
	(24, 32), (24, 32), (24, 32), (24, 32), # running right
	(24, 32), (24, 32), (24, 32), # jumping right
	(24, 32), # stading left
	(24, 32), (24, 32), (24, 32), (24, 32), # running left
	(24, 32), (24, 32), (24, 32), # jumping left
	(24, 32), (24, 32), # reload
	(40, 16), (40, 16), (40, 16), (40, 16), (40, 16), (40, 16), (40, 16), (40, 16), (40, 16), # ammo
	(32, 32), (32, 32), (24, 32), (24, 32),	(24, 32), (24, 32), #aim right 
	(32, 32), (32, 32), (24, 32), (24, 32),	(24, 32), (24, 32), # aim left
	(24, 32), (24, 32), (24, 32), (24, 32), # leaving
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 16),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(16, 8),
	(24, 16), # 1UP
	(16, 16), (16, 16), (16, 16), (16, 16), # chunks
	(16, 16), (16, 16), (16, 16), (16, 16), # chunks
]

SPRITE_SIZES_CHUNK1 = [
	(24, 40), # walk(4)
	(24, 40),
	(24, 40),
	(24, 40),
	(32, 40), # hit(3)
	(24, 40),
	(40, 40),
#	BREAKER,
	(24, 40), # walk(4)
	(24, 40),
	(24, 40),
	(24, 40),
	(32, 40), # hit(3)
	(24, 40),
	(40, 40),
#	BREAKER,
	(24, 40), # climb(2)
	(24, 40),

	(8, 16),  # alignment??

	(24, 24), # walk(4)
	(24, 24),
	(24, 24),
	(24, 24),
	(24, 24), # walk(4)
	(24, 24),
	(24, 24),
	(24, 24),

	(32, 24), # throw(2)
	(32, 24),

	(40, 24), # attack(4)
	(32, 24),
	(32, 24),
	(32, 24),
]

SPRITE_SIZES_CHUNK2 = [
	(24, 32),
	(24, 32),
	(24, 32),
	(24, 32),
	(24, 32),
	(24, 32),
	(24, 32),

	(8, 16),  # alignment

	(24, 8),  # slime(16)
	(24, 8),
	(24, 8),
	(24, 8),
	(24, 8),
	(24, 8),
	(24, 8),
	(24, 8),
	(24, 16),
	(24, 16),
	(24, 16),
	(24, 16),
	(24, 16),
	(24, 16),
	(24, 16),
	(24, 16),

	(8, 16),  # alignment

	(32, 8), 
	(32, 8), 
	(32, 8), 
	(32, 8), 

	(16, 24), 
	(8, 8), 

	(8, 16),  # alignment

	(24, 16), # flame
	(24, 16),
	(24, 16),
	(24, 16),

	(8, 16),  # alignment

	(32, 32), # wolf
	(32, 32), 
	(32, 32), 
	(32, 32), 
	(40, 24), 
	(32, 32), 
	(32, 32), 
	(32, 32), 
	(32, 32), 
	#(40, 24), 
]

SPRITE_SIZES_MASTER = [

	(72, 80),
	(72, 80),

	(24, 24),
	(24, 24),
	(24, 24),
	(24, 24),

	(64, 56),
	(64, 56),
	(64, 56),

	(104, 48)
]

SPRITE_SIZES_FRANK = [
	(56, 80),
	(32, 80),
	(56, 80),
	(32, 80),
	(56, 80),
	(32, 80),
	(56, 80),
	(32, 80),
	(16, 16),
	(16, 16),
]

INDEX = {
	's_dave' : SPRITE_SIZES_DAVE,
	's_chunk1' : SPRITE_SIZES_CHUNK1,
	's_chunk2' : SPRITE_SIZES_CHUNK2,
	's_master' : SPRITE_SIZES_MASTER,
	's_frank' : SPRITE_SIZES_FRANK
}

for key in INDEX:
	shuffled = open(key, "rb").read();

	SPRITE_SIZES = INDEX[key]
	print "Master: %s, items: %d" % (key, len(SPRITE_SIZES))

	MAGIC = ord(shuffled[0]) | (ord(shuffled[1]) << 8)
	shuffled = shuffled[10:]

	totalw = 0
	for i in range(len(SPRITE_SIZES)):
		dim = SPRITE_SIZES[i]
		totalw = totalw + dim[0]

	im = Image.new("P", (1024, 1024))
	im.im.putpalette("RGB", ega_palette.palette)

	x = 0
	y = 0	
	maxx = 0
	maxh = 0

	data = ""
	offset = 0
	for j in range(len(SPRITE_SIZES)):
	
		dim = SPRITE_SIZES[j]
		if dim == BREAKER:
			# line breaker
			x = 0
			y = y + maxh
			maxh = 0
			continue

		w = dim[0]
		h = dim[1]
		if h > maxh:
			maxh = h

       		nextoffset = offset + (w*h/8)

		#print "offset 0x%x (%d) to 0x%x (%d)" % (offset, offset, nextoffset, nextoffset)

		data = ""
		for i in range(4):
			dummy = shuffled[MAGIC*i + offset: MAGIC*i + nextoffset]
			data = data + dummy

		offset = nextoffset

		put_tile(im, data, x, y, w, h)
		x = x + w

		if x > maxx:
			maxx = x

	im = im.crop((0, 0, maxx, y + maxh))
	im.save("%s.png" % key)
