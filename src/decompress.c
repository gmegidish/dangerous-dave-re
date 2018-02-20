#include <stdio.h>
#include <assert.h>

const int ROOT = (254*2);
const int LUT_TAG = 0x100;

int main(int argc, char *argv[])
{
	FILE *fp;
	int src, dst, i;
	char signature[4];
	long unpacked_size;
	int bit;
	char out_filename[64];
	char *suffix;
	unsigned short leaf;
	unsigned short lut[255*2];
	int cdata_length;
	unsigned char cdata[64000];
	unsigned char value;
	unsigned char data[64000];
	
	if (argc != 2)
	{
		printf("Syntax: %s <HUFF file>", argv[0]);
		return 1;
	}

	fp = fopen(argv[1], "rb");

	/* must be HUFF */
	fread(signature, 4, 1, fp);
	if (strncmp(signature, "HUFF", 4) != 0)
	{
		printf("Tried to expand a file that isn't HUFF!\n");
		return 1;
	}

	/* number of bytes when unpacked */
	fread(&unpacked_size, 4, 1, fp);

	/* read the huffman lookup tree */
	fread(&lut, 255*2*2, 1, fp);

	assert(ftell(fp) == 0x404);
	cdata_length = fread(cdata, 1, sizeof(cdata), fp);
	fclose(fp);

	memset(data, 0xcc, sizeof(data));

	printf("packed size %d\n", cdata_length);
	printf("unpacked size %d\n", unpacked_size);

	src = 0;
	dst = 0;
	leaf = ROOT;
	bit = 1;

	value = cdata[src++];
	while (dst < unpacked_size)
	{
		unsigned short dx;

		if ((value & bit) == 0)
		{
			/* left */
			assert(leaf <= 255*2);
			dx = lut[leaf];
		}
		else
		{
			/* right */
			assert((leaf+1) <= 255*2);
			dx = lut[leaf + 1];
		}

		bit = bit << 1;
		if (bit == 0x100)
		{
			/* overflow, read another byte */
			bit = 1;
			value = cdata[src++];
		}

		if (dx >= LUT_TAG)
		{
			dx = dx - LUT_TAG;
			leaf = dx * 2;
		}
		else
		{
			/* decompressed a byte */
			data[dst++] = (dx & 0xff);
			leaf = ROOT;
		}
	}

	assert(dst == unpacked_size);

	strcpy(out_filename, argv[1]);
	suffix = strchr(out_filename, '.');
	*suffix = '\0';
	
	fp = fopen(out_filename, "wb");
	fwrite(data, 1, dst, fp);
	fclose(fp);

	return 0;
}
