from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
from secrets import flag

BLOCK_SIZE = 16

class PRNG(object):
	def __init__(self, seed):
		self.seed = seed
	
	@staticmethod
	def rotl(x, k):
		return ((x << k) & 0xffffffffffffffff) | (x >> 64 - k)
	
	def next(self):
		s0 = self.seed[0]
		s1 = self.seed[1]

		result = (s0 + s1) & 0xffffffffffffffff
		
		s1 ^= s0

		self.seed[0] = self.rotl(s0, 55) ^ s1 ^ ((s1 << 14) & 0xffffffffffffffff)
		self.seed[1] = self.rotl(s1, 36)
		return (result)

key = urandom(BLOCK_SIZE)

cipher = AES.new(key, AES.MODE_ECB)
flag_enc = cipher.encrypt(pad(flag, BLOCK_SIZE)).hex()

#print(key.hex())
print(f"{flag_enc=}")

seed1 = bytes_to_long(key[: BLOCK_SIZE//2])
seed2 = bytes_to_long(key[BLOCK_SIZE//2: ])

myRNG = PRNG([seed1, seed2])
key2 = bytes.fromhex(hex(myRNG.next())[2:] + hex(myRNG.next())[2:])

msg = b"Forward Secrecy is The Real Deal! No 0ne will get our secret now"
cipher2 = AES.new(key2, AES.MODE_ECB )
msg_enc = cipher2.encrypt(pad(msg, BLOCK_SIZE)).hex()
print(f"key2 ='{key2.hex()}'")
print(f"{msg_enc=}")


"""
flag_enc='b976ccb56a1231389b4cc16a0360843014decdf2cd8235be270d1cdfa56a56cceb6f835630452cc0eabfaa28cf7bfe3e234b51155364022a7b658a1ea68ec9c0'
key2 ='81c259b71a7d8b1df167fe238cc78bf6'
msg_enc='b23703d05c702fec1616349c3274e2a6171d77a1bd868272681e699ade6ccc74f703cbdb9b0558cdac27ecbfbe2b14754de6c3c02bfc4716f8c9efd2f4dc52422b37f28cd5a216808f974bff897708cc'
"""
