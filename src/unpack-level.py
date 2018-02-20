import sys

infile = sys.argv[1]
outfile = sys.argv[2]

f = open(infile, "rb")
rle = f.read()
f.close()

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

f = open(outfile, "wb")
f.write(raw)
f.close()
