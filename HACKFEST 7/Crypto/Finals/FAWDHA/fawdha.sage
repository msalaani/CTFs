#!/usr/bin/env sage

"""

Author : msalaani
Task : Fawdha - Challenge
Event : Hackfest 7 - Finals

"""

from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import random
import hashlib
from Crypto.Util.number import *

try:
	from secret import FLAG
except ImportError:
    FLAG = b"HACKFEST{DuMmy Flag for Dummy .... test}"

class CPRNG:
    def __init__(self,  mod, seed = None, nbits = 512) -> None:
        self.state = seed if seed else random.randint(1, 1 << nbits - 1)
        self.alpha = random.randint(1, 1 << nbits - 1)
        self.beta = random.randint(1, 1 << nbits - 1)
        self.mod = mod
    
    def next(self):
        self.state = self.alpha * self.state * (1 - self.state) + self.beta
        return self.state % self.mod
    
    def __repr__(self) -> str:
        return f"""alpha = {hex(self.alpha)}
beta = {hex(self.beta)}
        """
    
class ECDSA:
    def __init__(self, nbits = 521) -> None:
        p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        self.ec = EllipticCurve(GF(p), (
            0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc,
            0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
            ))
        self.G = self.ec(
            0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
            0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650
            )
        self.n = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409
        self.key = random.randint(1, 1 << nbits)
        self.csprng = CPRNG(self.n, self.key)
        
    
    def sign(self, msg):
        h = int.from_bytes(hashlib.sha256(msg).digest(), byteorder = "big")
        k = self.csprng.next()
        r = int((k * self.G).xy()[0])
        s = (inverse(k, self.n) * (h + r * self.key)) % self.n
        return r, s

def encrypt_flag(msg, key):
    key = hashlib.sha256(str(key).encode()).digest()[:16]
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pad(msg, 16)).hex()


if __name__ == "__main__" :
    ecdsa = ECDSA()
    msg = b"You signed it. Ma3ejbetnich 3aweeeed 3aweeed!"
    ecdsa.sign(msg)
    r, s = ecdsa.sign(msg)

    enc_flag = encrypt_flag(FLAG, ecdsa.key)

    print(ecdsa.csprng)
    print(f"r = {hex(r)}")
    print(f"s = {hex(s)}")
    print(f"{enc_flag = }")

    """
    alpha = 0x6a0bab0492c2ec87298e71bb6fbbefadf20b7692e9dbcec8fbc490122eec1bab37bc8a9feedc8508532d79483bc3d1edefd21d7c490178a1469fd709787d9b2
    beta = 0x1423c84ca7b4735e59910a09b42b8001ecd1d4d5dc7f8fc582012599a1ce5b4b2d69eaf727fc821b54b312596a5f639d9e50a9ba1d9c1d8c2c9f5df83657d167
            
    r = 0x5ce7b426db1b939092097097cd015ab5cdb0ae3620370cab2404b38c33c1e6e21acd5c023087f0160fb768eb6df94337ede12c68ae966355b82d309f8eaa93592e
    s = 0xaea8afbb585e6c03609851b76d013534cf73bdd1274fb88e0f583fb73fa44f676ce54331ce2a611a5728632926d0707719e322c0c34a132554ae9b9767bf4e8ff7
    enc_flag = '8698f8be6cac3e66c96c474dfeb574fd3a318c265ead2f9f49886e77f1933a4e0cdff2ec623ce62f5f4b0ea06a3457637644697c84e6fda1c90b869b4aba5d3da344eb99acba6cef1ef67886bd57d91b'
        
    """
