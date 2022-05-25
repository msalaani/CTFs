from Crypto.Util.number import *
from secrets import flag, N, e

def encrypt(m, N, e):

	assert type(m) == int

	for fi in bin(m)[2:]:
		x = getPrime(128)

		yield pow(pow(2, x + int(fi)) * pow(x + int(fi), 2), e, N)

m = bytes_to_long(flag)

ENC_B = []

for benc in encrypt(m, N, e):
	ENC_B.append(benc)

# I think that's all you need
print(f"{N = }")
print(f"{ENC_B = }")