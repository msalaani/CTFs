#!/usr/bin/env sage

"""

Author : msalaani
Task : FAWDHA - Solver
Event : Hackfest 7 - Finals

"""

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import random
import hashlib
from Crypto.Util.number import *

def decrypt_flag(msg, key):
    key = hashlib.sha256(str(key).encode()).digest()[:16]
    aes = AES.new(key, AES.MODE_ECB)
    return unpad(aes.decrypt(msg), 16)



msg = b"You signed it. Ma3ejbetnich 3aweeeed 3aweeed!"
h = int.from_bytes(hashlib.sha256(msg).digest(), byteorder = "big")

n = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
alpha = 0x6a0bab0492c2ec87298e71bb6fbbefadf20b7692e9dbcec8fbc490122eec1bab37bc8a9feedc8508532d79483bc3d1edefd21d7c490178a1469fd709787d9b2
beta = 0x1423c84ca7b4735e59910a09b42b8001ecd1d4d5dc7f8fc582012599a1ce5b4b2d69eaf727fc821b54b312596a5f639d9e50a9ba1d9c1d8c2c9f5df83657d167
        
r = 0x5ce7b426db1b939092097097cd015ab5cdb0ae3620370cab2404b38c33c1e6e21acd5c023087f0160fb768eb6df94337ede12c68ae966355b82d309f8eaa93592e
s = 0xaea8afbb585e6c03609851b76d013534cf73bdd1274fb88e0f583fb73fa44f676ce54331ce2a611a5728632926d0707719e322c0c34a132554ae9b9767bf4e8ff7
enc_flag = bytes.fromhex('8698f8be6cac3e66c96c474dfeb574fd3a318c265ead2f9f49886e77f1933a4e0cdff2ec623ce62f5f4b0ea06a3457637644697c84e6fda1c90b869b4aba5d3da344eb99acba6cef1ef67886bd57d91b')



coeffs = [
    -alpha^3*s,
    2*alpha^3*s,
    - (alpha^3*s - 2*alpha^2*beta*s + alpha^2*s),
    - (2*alpha^2*beta*s - alpha^2*s + r),
    - alpha*beta^2*s + beta*s + alpha*beta*s - h
]


bound = 1 << int(521 / 6)
P.<x> = PolynomialRing(Integers(n), "x")
monomials = [x^4, x^3, x^2, x, 1]
f = sum(coeff*monomial for coeff, monomial in zip(coeffs, monomials))
key  = f.roots(multiplicities = False)[0] #f.monic().small_roots(X = bound , epsilon=1/25)[0] # small_roots(f, (bounds,), d = 20, m = 7)[0] # defunds's coppersmith
assert key == 18416832431838432107397
assert decrypt_flag(enc_flag, key) == b"HACKFEST{d31fF31c64f09D1D00240963C56bDCFd685E659D5EfAfd93258D8dB20318a38f}"