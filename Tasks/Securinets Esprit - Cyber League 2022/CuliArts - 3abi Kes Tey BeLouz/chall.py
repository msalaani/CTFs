from ctypes import *
from secrets import secret_menu
import random

def pad(m, blocksize = 8):
	return m+bytes([blocksize-len(m)%blocksize])*(blocksize - len(m)%blocksize)

class KesTeyBeLouz:

	def __init__(self, key, blocksize = 8):
		self.key = key
		self.BLOCK_SIZE = blocksize
	
	def __t2bl(self, pt):
		assert len(pt) % self.BLOCK_SIZE == 0, "Data length is not in Block Size bound."

		blocks = [int.from_bytes(pt[i: i+self.BLOCK_SIZE // 2], "big") for i in range(0, len(pt), self.BLOCK_SIZE // 2)]
		return blocks
	
	def __bl2t(self, blocks):
		pt = b"".join(x.to_bytes(self.BLOCK_SIZE // 2, 'big') for x in blocks)

		assert len(pt) % self.BLOCK_SIZE == 0, "Data length is not in Block Size bound."
		return pt

	def __encrypt(self, block):
		y = c_uint32(block[0])
		z = c_uint32(block[1])
		sum = c_uint32(0)
		delta = 0x9e3779b9

		n = 32
		w = [0,0]

		while(n>0):
			sum.value += delta
			y.value += ( z.value << 4 ) + self.key[0] ^ z.value + sum.value ^ ( z.value >> 5 ) + self.key[1]
			z.value += ( y.value << 4 ) + self.key[2] ^ y.value + sum.value ^ ( y.value >> 5 ) + self.key[3]
			n -= 1

		w[0] = y.value
		w[1] = z.value
		return w

	def encrypt(self, pt):
		pt_blocks = self.__t2bl(pt)

		enc = []
		for i in range(0, len(pt_blocks), 2):
			ptblock = [pt_blocks[i], pt_blocks[i+1]]
			block_enc = self.__encrypt(ptblock)
			enc.append(block_enc[0])
			enc.append(block_enc[1])

		return self.__bl2t(enc)

def keygen(ind):
	key = [107, 215, 222, 69]
	r = random.randint(0, 255)
	key[ind] ^= r
	return bytes([ k for k in key])

Menu_lfa9r = [
	b"7th April 2022\n UniRestau: 3ejja Blech 3dham",
	b"8th April 2022\n UniRestau: Ma9rouna Bidha",
	secret_menu
]

secret = pad(Menu_lfa9r[2])
for i in range(4): # Multiple Encryption To Keep Me Away From Koujina :)
	key = keygen(i)
	cipher = KesTeyBeLouz(key)
	secret = cipher.encrypt(secret)
	

print(secret.hex())
# 2403b5bad11a6ca3b04a379b87630967c3f5c0526b5449b236f793ca225411087f7b0b1abcd2ce8f96ae6d843837b0aa30b48457d51ec6c0e062fd15bfa51b446dc6eb2219067c6f6dfe5489f38917e61acb56639f381eeac2b1d896a9c2bedef1149285af0d655e4f3e983f8dec9e2fac80066d29d5a69cfd2eee3946d906851d3f9dd2232c5714ad84c768ae01c80047bdd2eeaeb9dc25
