import random
from PIL import Image
from secrets import flag

def r2p(n):
	return n & 0xff, (n >> 8) & 0xff, (n >> 16) & 0xff, (n >> 24) & 0xff

def byte2bin(m):
	b = [bin(byte)[2:].zfill(8) for byte in m]
	b = [int(bit) for _ in b for bit in _]
	return b

flag_bits = byte2bin(flag)

width, height = 650, 2

img = Image.new( 'RGBA', (width,height), "white")
pixels = img.load()

for _h in range(height):
	for _w in range(width):
		xkey = random.getrandbits(32)
		xr, xg, xb, xa = r2p(xkey)
		pixels[_w,_h] = ((_w & 0xff) ^ xr, _h ^ xg, ((_w*_h) & 0xff) ^ xb, ((_w+_h) & 0xff) ^ xa )

		if _h & 1 == 1:
			p_ind = _w % 4
			pixel = list(pixels[_w,_h])
			pixel[p_ind] ^= flag_bits[_w % len(flag_bits)]
			pixels[_w,_h] = tuple(pixel)

img.save("flag.enc.png", "PNG")
